from fastapi import APIRouter, Depends, status
# from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.schemas.stock import StockIn, StockOut
from app.services.stock import StockService

router = APIRouter(tags=["Stock"], prefix="/stock")


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_stock(
    stock_data: StockIn,
    session: AsyncSession = Depends(get_session),
):
    return await StockService.create_stock(stock_data, session)


@router.get("/get_by_id/{stock_id}", status_code=status.HTTP_200_OK)
async def get_stock_by_id(
    stock_id: int,
    session: AsyncSession = Depends(get_session),
) -> StockOut:
    return await StockService.get_stock_by_id(stock_id, session)


@router.get("/get_all", status_code=status.HTTP_200_OK)
async def get_all_stocks(session: AsyncSession = Depends(get_session)) -> list[StockOut]:
    return await StockService.get_all_stocks(session)


@router.delete("/delete_by_id/{stock_id}", status_code=status.HTTP_200_OK)
async def delete_stock_by_id(
    stock_id: int,
    session: AsyncSession = Depends(get_session),
):
    return await StockService.delete_stock_by_id(stock_id, session)



