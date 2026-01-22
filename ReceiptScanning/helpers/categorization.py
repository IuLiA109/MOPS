from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from models.categories import Category
from models.categorization_rules import CategorizationRule
from models.merchants import Merchant
from models.user_merchant_preferences import UserMerchantPreference

# automatic categorization based on keywords and user preferences
class CategorizationService:    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def categorize_transaction(
        self, 
        user_id: int, 
        merchant_name: Optional[str], 
        description: Optional[str],
        transaction_type: str
    ) -> Optional[int]:

        # 1 user specific merchant preferences
        if merchant_name:
            merchant_id = await self._get_or_create_merchant(merchant_name)
            if merchant_id:
                category_id = await self._get_user_merchant_preference(user_id, merchant_id)
                if category_id:
                    return category_id
                
        # 2 check merchant default category
                category_id = await self._get_merchant_default_category(merchant_id)
                if category_id:
                    return category_id
        
        # 3 keyword based categorization rules
        text_to_analyze = f"{merchant_name or ''} {description or ''}".lower()
        category_id = await self._apply_keyword_rules(text_to_analyze, transaction_type)
        if category_id:
            return category_id
        
        # 4 default category for transaction type
        return await self._get_default_category(transaction_type)
    
    # helper to get/create merchant
    async def _get_or_create_merchant(self, merchant_name: str) -> Optional[int]:
        normalized = merchant_name.lower().strip()
        
        result = await self.db.execute(select(Merchant).where(Merchant.normalized_name == normalized))
        merchant = result.scalar_one_or_none()
        
        if not merchant:
            merchant = Merchant(
                normalized_name=normalized,
                display_name=merchant_name
            )
            self.db.add(merchant)
            await self.db.flush()
        
        return merchant.id
    
    # helper to get user preference for merchant
    async def _get_user_merchant_preference(self, user_id: int, merchant_id: int) -> Optional[int]:
        result = await self.db.execute(select(UserMerchantPreference).where(
            UserMerchantPreference.user_id == user_id,
            UserMerchantPreference.merchant_id == merchant_id
        ))
        preference = result.scalar_one_or_none()
        
        return preference.category_id if preference else None
    
    # helper to get merchant's default category
    async def _get_merchant_default_category(self, merchant_id: int) -> Optional[int]:
        merchant = await self.db.get(Merchant, merchant_id)
        return merchant.default_category_id if merchant else None
    
    # helper to apply keyword rules
    async def _apply_keyword_rules(self, text: str, transaction_type: str) -> Optional[int]:
        result = await self.db.execute((
            select(CategorizationRule)
            .join(Category)
            .where(
                CategorizationRule.is_active == True,
                Category.type == transaction_type
            ).order_by(CategorizationRule.priority.desc())
        ))
        
        rules = result.scalars().all()
        
        for rule in rules:
            if rule.keyword.lower() in text:
                return rule.category_id
        
        return None
    
    # helper to get system default category for transaction type
    async def _get_default_category(self, transaction_type: str) -> Optional[int]:
        result = await self.db.execute(select(Category).where(
            Category.is_system == True,
            Category.type == transaction_type,
            Category.name == "Diverse"  # Default "Other" category
        ))
        category = result.scalar_one_or_none()
        
        return category.id if category else None
    
    # learn from user's correction
    async def learn_from_correction(
        self, 
        user_id: int, 
        merchant_id: Optional[int], 
        new_category_id: int
    ):
        if not merchant_id:
            return
        
        result = await self.db.execute(select(UserMerchantPreference).where(
            UserMerchantPreference.user_id == user_id,
            UserMerchantPreference.merchant_id == merchant_id
        ))
        preference = result.scalar_one_or_none()
        
        if preference:
            preference.category_id = new_category_id
            preference.confidence = min(preference.confidence + 0.1, 1.0)
        else:
            preference = UserMerchantPreference(
                user_id=user_id,
                merchant_id=merchant_id,
                category_id=new_category_id,
                confidence=0.5
            )
            self.db.add(preference)
        
        await self.db.flush()

# functions to create default categories and rules
async def create_default_categories(db: AsyncSession):
    default_categories = [
        # expense categories
        {"name": "Supermarket", "type": "expense", "is_system": True},
        {"name": "Restaurante", "type": "expense", "is_system": True},
        {"name": "Transport", "type": "expense", "is_system": True},
        {"name": "Utilitati", "type": "expense", "is_system": True},
        {"name": "Sanatate", "type": "expense", "is_system": True},
        {"name": "Educatie", "type": "expense", "is_system": True},
        {"name": "Divertisment", "type": "expense", "is_system": True},
        {"name": "Diverse", "type": "expense", "is_system": True},
        
        # income categories
        {"name": "Salariu", "type": "income", "is_system": True},
        {"name": "Freelance", "type": "income", "is_system": True},
        {"name": "Diverse", "type": "income", "is_system": True},
    ]
    
    for cat_data in default_categories:
        result = await db.execute(select(Category).where(
            Category.name == cat_data["name"],
            Category.type == cat_data["type"],
            Category.is_system == True,
            Category.user_id == None
        ))

        existing = result.scalar_one_or_none()
        
        if not existing:
            category = Category(**cat_data, user_id=None)
            db.add(category)
    
    await db.commit()

# create default categorization rules
async def create_default_rules(db: AsyncSession):
    # get category IDs
    categories = {}
    result = await db.execute(select(Category).where(Category.is_system == True))
    for cat in result.scalars():
        categories[cat.name] = cat.id
    
    default_rules = [
        {"keyword": "kaufland", "category": "Supermarket", "priority": 10},
        {"keyword": "lidl", "category": "Supermarket", "priority": 10},
        {"keyword": "carrefour", "category": "Supermarket", "priority": 10},
        {"keyword": "mega", "category": "Supermarket", "priority": 10},
        {"keyword": "auchan", "category": "Supermarket", "priority": 10},
        
        {"keyword": "mcdonald", "category": "Restaurante", "priority": 10},
        {"keyword": "kfc", "category": "Restaurante", "priority": 10},
        {"keyword": "restaurant", "category": "Restaurante", "priority": 5},
        {"keyword": "pizza", "category": "Restaurante", "priority": 5},
        
        {"keyword": "omv", "category": "Transport", "priority": 10},
        {"keyword": "petrom", "category": "Transport", "priority": 10},
        {"keyword": "uber", "category": "Transport", "priority": 10},
        {"keyword": "bolt", "category": "Transport", "priority": 10},
        {"keyword": "taxi", "category": "Transport", "priority": 5},
        
        {"keyword": "enel", "category": "Utilități", "priority": 10},
        {"keyword": "digi", "category": "Utilități", "priority": 10},
        {"keyword": "orange", "category": "Utilități", "priority": 10},
        {"keyword": "vodafone", "category": "Utilități", "priority": 10},
    ]
    
    for rule_data in default_rules:
        category_name = rule_data["category"]
        if category_name not in categories:
            continue
        
        result = await db.execute(select(CategorizationRule).where(
            CategorizationRule.keyword == rule_data["keyword"],
            CategorizationRule.category_id == categories[category_name]
        ))
        existing = result.scalar_one_or_none()
        
        if not existing:
            rule = CategorizationRule(
                keyword=rule_data["keyword"],
                category_id=categories[category_name],
                priority=rule_data["priority"],
                is_active=True
            )
            db.add(rule)
    
    await db.commit()
