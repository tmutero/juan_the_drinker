from app.models.bar import Bar
from app.models.drink import Drink
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.daos.base import BaseDao
from app.models.visit import Visit
from sqlalchemy.sql import between

class VisitDao(BaseDao):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def create(self, visit_data) -> Visit:
        _visit = Visit(**visit_data)
        self.session.add(_visit)
        await self.session.commit()
        await self.session.refresh(_visit)
        return _visit
    

    async def create_drink(self, drink_data) -> Drink:
        _drink = Drink(**drink_data)
        self.session.add(_drink)
        await self.session.commit()
        await self.session.refresh(_drink)
        return _drink
    

    async def get_by_id(self, visit_id: int) -> Visit | None:
        statement = select(Visit).where(Visit.visit_id == visit_id)
        return await self.session.scalar(statement=statement)
    
    
    async def get_visits_by_bar_id(self, bar_id: int) -> Visit | None:
        statement = select(Visit).where(Visit.bar_id == bar_id)
        result = await self.session.execute(statement=statement)
        return result.scalars().all()
    
    async def get_drink_by_visit_id(self, visit_id: int) -> Drink | None:
        statement = select(Drink).where(Drink.visit_id == visit_id)
        return await self.session.scalar(statement=statement)


    async def get_by_name(self, name) -> Visit | None:
        statement = select(Visit).where(Visit.name == name)
        return await self.session.scalar(statement=statement)

    async def get_all(self, limit, offset ,start, end) -> list[Visit]:
        statement = select(Visit).where(between(Visit.visitedOn, start, end)).limit(limit).offset(offset).order_by(Visit.visit_id)
        result = await self.session.execute(statement=statement)
        return result.scalars().all()

    async def delete_all(self) -> None:
        await self.session.execute(delete(Visit))
        await self.session.commit()

    async def delete_by_id(self, visit_id: int) -> Visit | None:
        _visit = await self.get_by_id(visit_id=visit_id)
        statement = delete(Visit).where(Visit.visit_id == visit_id)
        await self.session.execute(statement=statement)
        await self.session.commit()
        return _visit
