from app.models.stock import Stock
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.daos.base import BaseDao
from app.models.bar import Bar


class BarDao(BaseDao):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def create(self, bar_data) -> Bar:
        _bar = Bar(**bar_data)
        self.session.add(_bar)
        await self.session.commit()
        await self.session.refresh(_bar)
        return _bar
    

    async def get_by_id(self, bar_id: int) -> Bar | None:
        # statement = select(Bar).where(Bar.bar_id == bar_id)
        statement = select(Bar).where(Bar.bar_id == bar_id).options(selectinload(Bar.stock)).order_by(Bar.bar_id)

        return await self.session.scalar(statement=statement)

    async def get_by_name(self, name) -> Bar | None:
        statement = select(Bar).where(Bar.name == name)
        return await self.session.scalar(statement=statement)

    async def get_all(self) -> list[Bar]:
        statement = select(Bar).options(selectinload(Bar.stock)).order_by(Bar.bar_id)
        result = await self.session.execute(statement=statement)
        return result.scalars().all()

    async def delete_all(self) -> None:
        await self.session.execute(delete(Bar))
        await self.session.commit()

    async def delete_by_id(self, bar_id: int) -> Bar | None:
        _bar = await self.get_by_id(bar_id=bar_id)
        statement = delete(Bar).where(Bar.bar_id == bar_id)
        await self.session.execute(statement=statement)
        await self.session.commit()
        return _bar
