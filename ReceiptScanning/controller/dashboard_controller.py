from typing import List, Dict, Any
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, extract

from db.session import get_db
from models.users import User
from models.transactions import Transaction
from models.categories import Category
from models.accounts import Account
from helpers.auth_dependencies import get_current_user

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

# get total income, expenses, balance, monthly stats
@router.get("/summary")
async def get_financial_summary(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # all time totals
    result = await db.execute(select(
        Transaction.type,
        func.sum(Transaction.amount).label("total")
    ).where(Transaction.user_id == current_user.id
    ).group_by(Transaction.type))
    
    totals = {row.type: float(row.total) for row in result}
    
    total_income = totals.get("income", 0)
    total_expenses = totals.get("expense", 0)
    balance = total_income - total_expenses
    
    # current month stats
    now = datetime.utcnow()
    first_day_of_month = datetime(now.year, now.month, 1)
    
    result = await db.execute(select(
        Transaction.type,
        func.sum(Transaction.amount).label("total")
    ).where(and_(
            Transaction.user_id == current_user.id,
            Transaction.transaction_date >= first_day_of_month
    )).group_by(Transaction.type))

    monthly_totals = {row.type: float(row.total) for row in result}
    
    monthly_income = monthly_totals.get("income", 0)
    monthly_expenses = monthly_totals.get("expense", 0)
    monthly_balance = monthly_income - monthly_expenses
    
    # how many accounts user has
    result = await db.execute(select(func.count(Account.id)).where(Account.user_id == current_user.id))
    account_count = result.scalar()
    
    # how many transactions user has
    result = await db.execute(select(func.count(Transaction.id)).where(Transaction.user_id == current_user.id))
    transaction_count = result.scalar()
    
    return {
        "all_time": {
            "total_income": total_income,
            "total_expenses": total_expenses,
            "balance": balance
        },
        "current_month": {
            "month": now.strftime("%B %Y"),
            "income": monthly_income,
            "expenses": monthly_expenses,
            "balance": monthly_balance
        },
        "stats": {
            "account_count": account_count,
            "transaction_count": transaction_count
        }
    }

# get expense distribution by category
@router.get("/expenses-by-category")
async def get_expenses_by_category(
    start_date: datetime = Query(None),
    end_date: datetime = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # default current month if no dates given
    if not start_date:
        now = datetime.utcnow()
        start_date = datetime(now.year, now.month, 1)
    
    if not end_date:
        end_date = datetime.utcnow()
    
    # expenses grouped by category
    result = await db.execute(select(
        Category.id,
        Category.name,
        func.sum(Transaction.amount).label("total"),
        func.count(Transaction.id).label("count")
    ).join(Transaction, Transaction.category_id == Category.id
    ).where(and_(
            Transaction.user_id == current_user.id,
            Transaction.type == "expense",
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date <= end_date
    )).group_by(Category.id, Category.name).order_by(func.sum(Transaction.amount).desc()))
    
    categories = result.all()
    
    # uncategorized transactions
    result = await db.execute(select(
        func.sum(Transaction.amount).label("total"),
        func.count(Transaction.id).label("count")
    ).where(
        and_(
            Transaction.user_id == current_user.id,
            Transaction.type == "expense",
            Transaction.category_id == None,
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date <= end_date
        )
    ))
    uncategorized = result.one()
    
    data = [
        {
            "category_id": cat.id,
            "category_name": cat.name,
            "total": float(cat.total),
            "transaction_count": cat.count,
            "percentage": 0
        }
        for cat in categories
    ]
    
    if uncategorized.total:
        data.append({
            "category_id": None,
            "category_name": "Necategorizat",
            "total": float(uncategorized.total),
            "transaction_count": uncategorized.count,
            "percentage": 0
        })
    
    # percentages
    total_expenses = sum(item["total"] for item in data)
    if total_expenses > 0:
        for item in data:
            item["percentage"] = round((item["total"] / total_expenses) * 100, 2)
    
    return {
        "period": {
            "start": start_date.isoformat(),
            "end": end_date.isoformat()
        },
        "total_expenses": total_expenses,
        "categories": data
    }

# income/expenses over time (monthly data for last N months)
@router.get("/income-vs-expenses")
async def get_income_vs_expenses(
    months: int = Query(6, ge=1, le=24),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    now = datetime.utcnow()
    start_date = now - timedelta(days=months * 31)
    
    # monthly aggregated data
    result = await db.execute(select(
        extract('year', Transaction.transaction_date).label('year'),
        extract('month', Transaction.transaction_date).label('month'),
        Transaction.type,
        func.sum(Transaction.amount).label('total')
    ).where(and_(
            Transaction.user_id == current_user.id,
            Transaction.transaction_date >= start_date
    )).group_by(
        extract('year', Transaction.transaction_date),
        extract('month', Transaction.transaction_date),
        Transaction.type
    ).order_by('year', 'month'))

    rows = result.all()
    
    # organize data by month
    monthly_data = {}
    for row in rows:
        year_month = f"{int(row.year)}-{int(row.month):02d}"
        if year_month not in monthly_data:
            monthly_data[year_month] = {"income": 0, "expenses": 0}
        
        if row.type == "income":
            monthly_data[year_month]["income"] = float(row.total)
        elif row.type == "expense":
            monthly_data[year_month]["expenses"] = float(row.total)
    
    data = []
    for year_month in sorted(monthly_data.keys()):
        year, month = year_month.split("-")
        month_name = datetime(int(year), int(month), 1).strftime("%B %Y")
        
        income = monthly_data[year_month]["income"]
        expenses = monthly_data[year_month]["expenses"]
        
        data.append({
            "period": year_month,
            "month_name": month_name,
            "income": income,
            "expenses": expenses,
            "balance": income - expenses
        })
    
    return {
        "months": months,
        "data": data
    }

# get recent transactions for dashboard
@router.get("/recent-transactions")
async def get_recent_transactions(
    limit: int = Query(10, ge=1, le=50),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Transaction
        ).where(Transaction.user_id == current_user.id
        ).order_by(Transaction.transaction_date.desc()).limit(limit))

    transactions = result.scalars().all()
    
    data = []
    for t in transactions:
        category_name = None
        if t.category_id:
            category = await db.get(Category, t.category_id)
            if category:
                category_name = category.name
        
        data.append({
            "id": t.id,
            "type": t.type,
            "amount": float(t.amount),
            "currency": t.currency,
            "description": t.description,
            "category_name": category_name,
            "transaction_date": t.transaction_date.isoformat()
        })
    
    return data
