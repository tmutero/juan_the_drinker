from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse

from jose import JWTError, jwt
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.daos import bar

from app.daos import stock
from app.db import get_session
from app.models.bar import Bar as BarModel
from app.schemas.bar import ChangeBarIn, BarIn, BarOut

class BarService:
    @staticmethod
    async def create_bar(bar_data: BarIn, session: AsyncSession):
        bar_exist = await BarService.bar_name_exists(session, bar_data.name)

        if bar_exist:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bar with the given name already exists!!!",
            )

        new_bar = await bar.BarDao(session).create(bar_data.model_dump())
        logger.info(f"New bar created successfully: {new_bar}!!!")
        return JSONResponse(
            content={"message": "Bar created successfully"},
            status_code=status.HTTP_201_CREATED,
        )

    @staticmethod
    async def bar_name_exists(session: AsyncSession, name: str) -> BarModel | None:
        _bar = await bar.BarDao(session).get_by_name(name)
        return _bar if _bar else None

    @staticmethod
    async def get_all_bars(session: AsyncSession) -> list[BarOut]:
        all_bars = await bar.BarDao(session).get_all()
        return all_bars

    @staticmethod
    async def delete_all_bars(session: AsyncSession):
        await bar.BarDao(session).delete_all()
        return JSONResponse(
            content={"message": "All bars deleted successfully!!!"},
            status_code=status.HTTP_200_OK,
        )

    @staticmethod
    async def get_bar_by_id(bar_id: int, session: AsyncSession) -> BarOut:
        _bar = await bar.BarDao(session).get_by_id(bar_id)
        if not _bar:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bar with the given id does not exist!!!",
            )
        return _bar 
    
    @staticmethod
    async def update_bar(
        bar_data: ChangeBarIn,
        session: AsyncSession = Depends(get_session),
    ):
        _bar = await bar.BarDao(session).get_by_id(bar_data.bar_id)
        if not _bar:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bar with the given id does not exist!!!",
            )
        _bar.name = bar_data.name
        _bar.address = bar_data.address

        session.add(_bar)
        await session.commit()
        return JSONResponse(
            content={"message": "Bar updated successfully!!!"},
            status_code=status.HTTP_200_OK,
        )

    @staticmethod
    async def delete_bar_by_id(bar_id: int, session: AsyncSession):
        _country = await bar.BarDao(session).delete_by_id(bar_id)
        if not _country:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bar with the given id does not exist!!!",
            )
        return JSONResponse(
            content={"message": "Bar deleted successfully!!!"},
            status_code=status.HTTP_200_OK,
        )
