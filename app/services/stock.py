from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse

from jose import JWTError, jwt
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.daos import stock
from app.db import get_session
from app.models.stock import Stock as StockModel
from app.schemas.stock import StockBase, StockIn, StockOut

class StockService:
    @staticmethod
    async def create_stock(stock_data: StockIn, session: AsyncSession):
        stock_exist = await StockService.stock_name_exists(session, stock_data.name)

        if stock_exist:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Stock with the given name already exists!!!",
            )

        new_stock = await stock.StockDao(session).create(stock_data.model_dump())
        logger.info(f"New stock created successfully: {new_stock}!!!")
        return JSONResponse(
            content={"message": "Stock created successfully"},
            status_code=status.HTTP_201_CREATED,
        )

    @staticmethod
    async def stock_name_exists(session: AsyncSession, name: str) -> StockModel | None:
        _stock = await stock.StockDao(session).get_by_name(name)
        return _stock if _stock else None

    @staticmethod
    async def get_all_stocks(session: AsyncSession) -> list[StockOut]:
        all_bars = await stock.StockDao(session).get_all()
        return all_bars


    @staticmethod
    async def get_stock_by_id(stock_id: int, session: AsyncSession) -> StockOut:
        _stock = await stock.StockDao(session).get_by_id(stock_id)
        if not _stock:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Stock with the given id does not exist!!!",
            )
        return _stock 
    

    @staticmethod
    async def delete_stock_by_id(stock_id: int, session: AsyncSession):
        _country = await stock.StockDao(session).delete_by_id(stock_id)
        if not _country:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bar with the given id does not exist!!!",
            )
        return JSONResponse(
            content={"message": "Bar deleted successfully!!!"},
            status_code=status.HTTP_200_OK,
        )
