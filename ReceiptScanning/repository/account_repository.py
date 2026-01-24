from typing import Optional, Tuple

from sqlalchemy import case, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.accounts import Account
from models.transactions import Transaction


class AccountRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_id(self, account_id: int, user_id: int) -> Optional[Account]:
        result = await self.db.execute(
            select(Account).where(Account.id == account_id, Account.user_id == user_id)
        )
        return result.scalars().first()

    async def get_with_balance(
        self, account_id: int, user_id: int
    ) -> Optional[Tuple[Account, float, int]]:
        account = await self.get_by_id(account_id, user_id)
        if not account:
            return None

        result = await self.db.execute(
            select(
                func.sum(
                    case(
                        (Transaction.type == "income", Transaction.amount),
                        else_=-Transaction.amount,
                    )
                ).label("balance"),
                func.count(Transaction.id).label("count"),
            ).where(Transaction.account_id == account.id)
        )

        balance_val, count_val = result.one()
        balance = float(balance_val) if balance_val is not None else 0.0
        transaction_count = int(count_val) if count_val is not None else 0

        return account, balance, transaction_count
