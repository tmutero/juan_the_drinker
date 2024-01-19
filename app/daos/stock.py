from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.daos.base import BaseDao
from app.models.stock import Stock


class StockDao(BaseDao):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def create(self, bar_data) -> Stock:
        _stock = Stock(**bar_data)
        self.session.add(_stock)
        await self.session.commit()
        await self.session.refresh(_stock)
        return _stock
    

    async def get_by_id(self, stock_id: int) -> Stock | None:
        statement = select(Stock).where(Stock.stock_id == stock_id)
        return await self.session.scalar(statement=statement)
    
    
    async def get_stock_by_bar_id(self, bar_id: int) -> Stock | None:
        statement = select(Stock).where(Stock.bar_id == bar_id)
        result = await self.session.execute(statement=statement)
        return result.scalars().all()

    async def get_by_name(self, name) -> Stock | None:
        statement = select(Stock).where(Stock.name == name)
        return await self.session.scalar(statement=statement)

    async def get_all(self) -> list[Stock]:
        statement = select(Stock).order_by(Stock.stock_id)
        result = await self.session.execute(statement=statement)
        return result.scalars().all()

    async def delete_all(self) -> None:
        await self.session.execute(delete(Stock))
        await self.session.commit()

    async def delete_by_id(self, stock_id: int) -> Stock | None:
        _stock = await self.get_by_id(stock_id=stock_id)
        statement = delete(Stock).where(Stock.stock_id == stock_id)
        await self.session.execute(statement=statement)
        await self.session.commit()
        return _stock
