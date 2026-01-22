from typing import List, Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, func, and_
from decimal import Decimal

from db.session import get_db
from models.users import User
from models.transactions import Transaction
from models.accounts import Account
from models.merchants import Merchant
from models.categories import Category
from schemas.transaction import TransactionCreate, TransactionUpdate, TransactionRead
from helpers.auth_dependencies import get_current_user
from helpers.categorization import CategorizationService

router = APIRouter(prefix="/transactions", tags=["transactions"])

# create transaction
@router.post("/", response_model=TransactionRead, status_code=201)
async def create_transaction(
    payload: TransactionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    type: expense, income, transfer
    """
    # check that account belongs to user
    account = await db.get(Account, payload.account_id)
    if not account or account.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Account not found")
    
    # init categorization service
    categorization_service = CategorizationService(db)
    
    # get or create merchant and auto-categorize
    merchant_id = None
    if payload.merchant_name:
        merchant_id = await categorization_service._get_or_create_merchant(payload.merchant_name)
    
    category_id = await categorization_service.categorize_transaction(
        user_id=current_user.id,
        merchant_name=payload.merchant_name,
        description=payload.description,
        transaction_type=payload.type
    )
    
    new_transaction = Transaction(
        user_id=current_user.id,
        account_id=payload.account_id,
        merchant_id=merchant_id,
        category_id=category_id,
        type=payload.type,
        amount=float(payload.amount),
        currency=payload.currency,
        transaction_date=payload.transaction_date,
        description=payload.description,
        source_type="manual"
    )
    
    db.add(new_transaction)
    await db.commit()
    await db.refresh(new_transaction)
    
    return await _build_transaction_read(new_transaction, db)

# list transactions with filters
@router.get("/", response_model=List[TransactionRead])
async def list_transactions(
    account_id: Optional[int] = Query(None),
    category_id: Optional[int] = Query(None),
    type: Optional[str] = Query(None, pattern="^(expense|income|transfer)$"),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    limit: int = Query(100, le=1000),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(Transaction).where(Transaction.user_id == current_user.id)
    
    if account_id:
        query = query.where(Transaction.account_id == account_id)
    if category_id:
        query = query.where(Transaction.category_id == category_id)
    if type:
        query = query.where(Transaction.type == type)
    if start_date:
        query = query.where(Transaction.transaction_date >= start_date)
    if end_date:
        query = query.where(Transaction.transaction_date <= end_date)
    
    query = query.order_by(Transaction.transaction_date.desc())
    query = query.offset(offset).limit(limit)
    
    result = await db.execute(query)
    transactions = result.scalars().all()
    
    return [await _build_transaction_read(t, db) for t in transactions]

# get transaction by id
@router.get("/{transaction_id}", response_model=TransactionRead)
async def get_transaction(
    transaction_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    transaction = await db.get(Transaction, transaction_id)
    
    if not transaction or transaction.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    return await _build_transaction_read(transaction, db)

# update transaction (if category changed, learn from correction)
@router.put("/{transaction_id}", response_model=TransactionRead)
async def update_transaction(
    transaction_id: int,
    payload: TransactionUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    transaction = await db.get(Transaction, transaction_id)
    
    if not transaction or transaction.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    old_category_id = transaction.category_id
    
    if payload.amount is not None:
        transaction.amount = float(payload.amount)
    if payload.transaction_date is not None:
        transaction.transaction_date = payload.transaction_date
    if payload.description is not None:
        transaction.description = payload.description
    if payload.category_id is not None:
        transaction.category_id = payload.category_id
    
    # update seller if name provided
    if payload.merchant_name is not None:
        categorization_service = CategorizationService(db)
        merchant_id = await categorization_service._get_or_create_merchant(payload.merchant_name)
        transaction.merchant_id = merchant_id
    
    # learn from category change
    if payload.category_id is not None and payload.category_id != old_category_id:
        if transaction.merchant_id:
            categorization_service = CategorizationService(db)
            await categorization_service.learn_from_correction(
                user_id=current_user.id,
                merchant_id=transaction.merchant_id,
                new_category_id=payload.category_id
            )
    
    await db.commit()
    await db.refresh(transaction)
    
    return await _build_transaction_read(transaction, db)

# delete transaction
@router.delete("/{transaction_id}", status_code=204)
async def delete_transaction(
    transaction_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    transaction = await db.get(Transaction, transaction_id)
    
    if not transaction or transaction.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    await db.delete(transaction)
    await db.commit()
    
    return None

# helper to build TransactionRead
async def _build_transaction_read(transaction: Transaction, db: AsyncSession) -> TransactionRead:
    # related entities
    merchant_name = None
    if transaction.merchant_id:
        merchant = await db.get(Merchant, transaction.merchant_id)
        if merchant:
            merchant_name = merchant.display_name
    
    category_name = None
    if transaction.category_id:
        category = await db.get(Category, transaction.category_id)
        if category:
            category_name = category.name
    
    account_name = None
    if transaction.account_id:
        account = await db.get(Account, transaction.account_id)
        if account:
            account_name = account.name
    
    return TransactionRead(
        id=transaction.id,
        user_id=transaction.user_id,
        account_id=transaction.account_id,
        merchant_id=transaction.merchant_id,
        category_id=transaction.category_id,
        type=transaction.type,
        amount=Decimal(str(transaction.amount)),
        currency=transaction.currency,
        transaction_date=transaction.transaction_date,
        description=transaction.description,
        source_type=transaction.source_type,
        created_at=transaction.created_at,
        merchant_name=merchant_name,
        category_name=category_name,
        account_name=account_name
    )
