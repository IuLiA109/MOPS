from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, case

from db.session import get_db
from models.users import User
from models.accounts import Account
from models.transactions import Transaction
from schemas.account import AccountCreate, AccountUpdate, AccountRead, AccountWithBalance
from helpers.auth_dependencies import get_current_user

router = APIRouter(prefix="/accounts", tags=["accounts"])

# new account
@router.post("/", response_model=AccountRead, status_code=201)
async def create_account(
    payload: AccountCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # if new account is default, UNSET other default accounts
    if payload.is_default:
        result = await db.execute(select(Account).where(Account.user_id == current_user.id, Account.is_default == True))
        existing_defaults = result.scalars().all()
        
        for account in existing_defaults:
            account.is_default = False
    
    new_account = Account(
        user_id=current_user.id,
        name=payload.name,
        type=payload.type,
        currency=payload.currency,
        is_default=payload.is_default
    )
    
    db.add(new_account)
    await db.commit()
    await db.refresh(new_account)
    
    return new_account

# list accounts
@router.get("/", response_model=List[AccountRead])
async def list_accounts(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Account).where(Account.user_id == current_user.id).order_by(Account.is_default.desc(), Account.created_at))
    accounts = result.scalars().all()
    
    return accounts

# list accounts with balance sum(income) - sum(expenses) and transaction count
@router.get("/with-balance", response_model=List[AccountWithBalance])
async def list_accounts_with_balance(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Account).where(Account.user_id == current_user.id).order_by(Account.is_default.desc(), Account.created_at))
    accounts = result.scalars().all()
    
    accounts_with_balance = []
    for account in accounts:
        # sum(income) - sum(expenses) and count transactions
        result = await db.execute(select(
            func.sum(
                case(
                    (Transaction.type == "income", Transaction.amount),
                    else_=-Transaction.amount
                )
            ).label("balance"),
            func.count(Transaction.id).label("count")
        ).where(Transaction.account_id == account.id))
        
        balance_val, count_val = result.one()
        
        accounts_with_balance.append(
            AccountWithBalance(
                id=account.id,
                user_id=account.user_id,
                name=account.name,
                type=account.type,
                currency=account.currency,
                is_default=account.is_default,
                created_at=account.created_at,
                balance=float(balance_val) if balance_val else 0.0,
                transaction_count=int(count_val) if count_val else 0
            )
        )
    
    return accounts_with_balance

# get account by id
@router.get("/{account_id}", response_model=AccountRead)
async def get_account(
    account_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    account = await db.get(Account, account_id)
    
    if not account or account.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Account not found")
    
    return account

# update account by id
@router.put("/{account_id}", response_model=AccountRead)
async def update_account(
    account_id: int,
    payload: AccountUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    account = await db.get(Account, account_id)
    
    if not account or account.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Account not found")
    
    # if updated account is now default, UNSET other default accounts
    if payload.is_default is True and not account.is_default:
        result = await db.execute(select(Account).where(
            Account.user_id == current_user.id,
            Account.is_default == True,
            Account.id != account_id
        ))
        existing_defaults = result.scalars().all()
        
        for acc in existing_defaults:
            acc.is_default = False
    
    # Update fields
    if payload.name is not None:
        account.name = payload.name
    if payload.type is not None:
        account.type = payload.type
    if payload.currency is not None:
        account.currency = payload.currency
    if payload.is_default is not None:
        account.is_default = payload.is_default
    
    await db.commit()
    await db.refresh(account)
    
    return account

# delete account by id (only if no transactions)
@router.delete("/{account_id}", status_code=204)
async def delete_account(
    account_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    account = await db.get(Account, account_id)
    
    if not account or account.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Account not found")
    
    # first check if account has transactions
    result = await db.execute(select(func.count(Transaction.id)).where(Transaction.account_id == account_id))
    transaction_count = result.scalar() or 0
    
    if transaction_count > 0:
        raise HTTPException(
            status_code=400, 
            detail=f"Cannot delete account with {transaction_count} transactions. Delete transactions first."
        )
    
    await db.delete(account)
    await db.commit()
    
    return None
