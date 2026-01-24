from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, func

from db.session import get_db
from models.users import User
from models.categories import Category
from models.transactions import Transaction
from schemas.category import CategoryCreate, CategoryUpdate, CategoryRead, CategoryWithStats
from helpers.auth_dependencies import get_current_user, get_admin_user

router = APIRouter(prefix="/categories", tags=["categories"])

# new category
@router.post("/", response_model=CategoryRead, status_code=201)
async def create_category(
    payload: CategoryCreate,
    current_user: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db)
):
    if payload.type not in ['expense', 'income']:
        raise HTTPException(status_code=400, detail="Category type must be either 'expense' or 'income'")

    # check for existing category with same name and type
    result = await db.execute(select(Category).where(
        Category.user_id == current_user.id,
        Category.name == payload.name,
        Category.type == payload.type
    ))
    
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=409, 
            detail=f"Category '{payload.name}' already exists for {payload.type} transactions"
        )
    
    new_category = Category(
        user_id=current_user.id,
        name=payload.name,
        type=payload.type,
        is_system=False
    )
    
    db.add(new_category)
    await db.commit()
    await db.refresh(new_category)
    
    return new_category

# list categories
@router.get("/", response_model=List[CategoryRead])
async def list_categories(
    type: str = Query(None, pattern="^(expense|income)$"),
    include_system: bool = Query(True),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    query = select(Category).where(
        (Category.user_id == current_user.id) | 
        (Category.user_id == None if include_system else False)
    )
    
    if type:
        query = query.where(Category.type == type)
    
    query = query.order_by(Category.is_system.desc(), Category.name)
    
    result = await db.execute(query)
    categories = result.scalars().all()
    
    return categories

# get categories with stats
@router.get("/stats", response_model=List[CategoryWithStats])
async def get_categories_with_stats(
    type: str = Query(None, pattern="^(expense|income)$"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # all categories
    query = select(Category).where((Category.user_id == current_user.id) | (Category.user_id == None))
    
    if type:
        query = query.where(Category.type == type)
    
    result = await db.execute(query)
    categories = result.scalars().all()
    
    # stats for each category
    categories_with_stats = []
    for category in categories:
        result = await db.execute(select(
            func.count(Transaction.id).label("count"),
            func.sum(Transaction.amount).label("total")
        ).where(
            Transaction.user_id == current_user.id,
            Transaction.category_id == category.id
        ))
        
        count_val, total_val = result.one()
        
        categories_with_stats.append(
            CategoryWithStats(
                id=category.id,
                user_id=category.user_id,
                name=category.name,
                type=category.type,
                is_system=category.is_system,
                created_at=category.created_at,
                transaction_count=int(count_val) if count_val else 0,
                total_amount=float(total_val) if total_val else 0.0
            )
        )
    
    return categories_with_stats

# get category by id
@router.get("/{category_id}", response_model=CategoryRead)
async def get_category(
    category_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    category = await db.get(Category, category_id)
    
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # user can only access THEIR OWN categories or system categories
    if category.user_id != current_user.id and category.user_id is not None:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return category

# update category
@router.put("/{category_id}", response_model=CategoryRead)
async def update_category(
    category_id: int,
    payload: CategoryUpdate,
    current_user: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db)
):
    category = await db.get(Category, category_id)
    
    if not category or category.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Category not found")
    
    if category.is_system:
        raise HTTPException(status_code=403, detail="Cannot modify system categories")
    
    # check duplicate names
    if payload.name:
        result = await db.execute(select(Category).where(
            Category.user_id == current_user.id,
            Category.name == payload.name,
            Category.id != category_id
        ))
        if result.scalar_one_or_none():
            raise HTTPException(status_code=409, detail=f"Category '{payload.name}' already exists")
        
        category.name = payload.name
    
    if payload.type:
        category.type = payload.type
    
    await db.commit()
    await db.refresh(category)
    
    return category

# delete category by id
@router.delete("/{category_id}", status_code=204)
async def delete_category(
    category_id: int,
    current_user: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db)
):
    category = await db.get(Category, category_id)
    
    if not category or category.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Category not found")
    
    if category.is_system:
        raise HTTPException(status_code=403, detail="Cannot delete system categories")
    
    # check if category used in transactions
    result = await db.execute(select(func.count(Transaction.id)).where(Transaction.category_id == category_id))
    usage_count = result.scalar() or 0
    
    if usage_count > 0:
        # update transactions to set category_id to NULL
        result = await db.execute(select(Transaction).where(Transaction.category_id == category_id))
        transactions = result.scalars().all()
        
        for transaction in transactions:
            transaction.category_id = None
    
    await db.delete(category)
    await db.commit()
    
    return None
