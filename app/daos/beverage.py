from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.daos.base import BaseDao
from app.models.beverage import Beverage


class BeverageDao(BaseDao):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def create(self, bar_data) -> Beverage:
        _beverage = Beverage(**bar_data)
        self.session.add(_beverage)
        await self.session.commit()
        await self.session.refresh(_beverage)
        return _beverage
    

    async def get_by_id(self, beverage_id: int) -> Beverage | None:
        statement = select(Beverage).where(Beverage.beverage_id == beverage_id)
        return await self.session.scalar(statement=statement)

    async def get_by_name(self, name) -> Beverage | None:
        statement = select(Beverage).where(Beverage.name == name)
        return await self.session.scalar(statement=statement)

    async def get_all(self) -> list[Beverage]:
        statement = select(Beverage).order_by(Beverage.beverage_id)
        result = await self.session.execute(statement=statement)
        return result.scalars().all()

    async def delete_all(self) -> None:
        await self.session.execute(delete(Beverage))
        await self.session.commit()

    async def delete_by_id(self, beverage_id: int) -> Beverage | None:
        _beverage = await self.get_by_id(beverage_id=beverage_id)
        statement = delete(Beverage).where(Beverage.beverage_id == beverage_id)
        await self.session.execute(statement=statement)
        await self.session.commit()
        return _beverage
