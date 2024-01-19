from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse

from jose import JWTError, jwt
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.daos import beverage
from app.db import get_session
from app.models.beverage import Beverage as BeverageModel
from app.schemas.beverage import BeverageIn, BeverageOut

class BeverageService:
    @staticmethod
    async def create_beverage(beverage_data: BeverageIn, session: AsyncSession):
        beverage_exist = await BeverageService.beverages_name_exists(session, beverage_data.name)

        if beverage_exist:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Beverage with the given name already exists!!!",
            )

        new_beverage = await beverage.BeverageDao(session).create(beverage_data.model_dump())
        logger.info(f"New beverage created successfully: {new_beverage}!!!")
        return JSONResponse(
            content={"message": "Beverage created successfully"},
            status_code=status.HTTP_201_CREATED,
        )

    @staticmethod
    async def beverages_name_exists(session: AsyncSession, name: str) -> BeverageModel | None:
        _beverage = await beverage.BeverageDao(session).get_by_name(name)
        return _beverage if _beverage else None

    @staticmethod
    async def get_all_beverages(session: AsyncSession) -> list[BeverageOut]:
        all_bars = await beverage.BeverageDao(session).get_all()
        return all_bars

    @staticmethod
    async def delete_all_beverages(session: AsyncSession):
        await beverage.BeverageDao(session).delete_all()
        return JSONResponse(
            content={"message": "All beverages deleted successfully!!!"},
            status_code=status.HTTP_200_OK,
        )

    @staticmethod
    async def get_beverage_by_id(bar_id: int, session: AsyncSession) -> BeverageOut:
        _beverage = await beverage.BeverageDao(session).get_by_id(bar_id)
        if not _beverage:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Beverage with the given id does not exist!!!",
            )
        return _beverage 
    
   

    @staticmethod
    async def delete_beverage_by_id(bar_id: int, session: AsyncSession):
        _country = await beverage.BeverageDao(session).delete_by_id(bar_id)
        if not _country:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Beverage with the given id does not exist!!!",
            )
        return JSONResponse(
            content={"message": "Beverage deleted successfully!!!"},
            status_code=status.HTTP_200_OK,
        )
