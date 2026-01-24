from datetime import datetime
from decimal import Decimal
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from helpers.categorization import CategorizationService
from models.accounts import Account
from models.categories import Category
from models.merchants import Merchant
from models.products import Product
from models.receipts import Receipt
from models.transactions import Transaction
from schemas.receipt import ReceiptBaseModel
from schemas.transaction import TransactionRead


class TransactionService:
	def __init__(self, db: AsyncSession):
		self.db = db
		self.categorization = CategorizationService(db)

	async def create_with_receipt(
		self,
		user_id: int,
		account_id: int,
		receipt_payload: ReceiptBaseModel,
		transaction_type: str = "expense",
		description: Optional[str] = None,
		currency: str = "RON",
		transaction_date: Optional[datetime] = None,
		merchant_name: Optional[str] = None,
	) -> Transaction:
		account = await self.db.get(Account, account_id)
		if not account or account.user_id != user_id:
			raise HTTPException(status_code=404, detail="Account not found")

		amount = Decimal(str(receipt_payload.total or 0))
		if amount <= 0:
			raise HTTPException(status_code=400, detail="Receipt total must be greater than 0")

		merchant_id = None
		if merchant_name:
			merchant_id = await self.categorization._get_or_create_merchant(merchant_name)

		category_id = await self.categorization.categorize_transaction(
			user_id=user_id,
			merchant_name=merchant_name,
			description=description,
			transaction_type=transaction_type,
		)

		transaction = Transaction(
			user_id=user_id,
			account_id=account_id,
			merchant_id=merchant_id,
			category_id=category_id,
			type=transaction_type,
			description=description,
			amount=amount,
			currency=currency,
			transaction_date=transaction_date or datetime.utcnow(),
			source_type="receipt_scan",
		)

		transaction.receipt = Receipt(
			total=amount,
			raw_text=receipt_payload.raw_text,
			products=[
				Product(
					name=item.name,
					price=item.price,
					quantity=item.quantity,
					unit=item.unit,
					sale=item.sale,
				)
				for item in receipt_payload.product
			],
		)

		self.db.add(transaction)
		await self.db.commit()
		await self.db.refresh(transaction)
		return transaction

	async def build_transaction_read(self, transaction: Transaction) -> TransactionRead:
		merchant_name = None
		if transaction.merchant_id:
			merchant = await self.db.get(Merchant, transaction.merchant_id)
			if merchant:
				merchant_name = merchant.display_name

		category_name = None
		if transaction.category_id:
			category = await self.db.get(Category, transaction.category_id)
			if category:
				category_name = category.name

		account_name = None
		if transaction.account_id:
			account = await self.db.get(Account, transaction.account_id)
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
			account_name=account_name,
		)
