from fastapi import APIRouter, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.schemas.token import Token
from app.schemas.beverage import BeverageIn, BeverageOut
from app.services.beverage import BeverageService

router = APIRouter(tags=["Beverage"], prefix="/beverage")


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_beverage(
    beverage_data: BeverageIn,
    session: AsyncSession = Depends(get_session),
):
    return await BeverageService.create_beverage(beverage_data, session)


@router.get("/get_by_id/{beverage_id}", status_code=status.HTTP_200_OK)
async def get_beverage_by_id(
    beverage_id: int,
    session: AsyncSession = Depends(get_session),
) -> BeverageOut:
    return await BeverageService.get_beverage_by_id(beverage_id, session)


@router.get("/get_all", status_code=status.HTTP_200_OK)
async def get_all_beverages(session: AsyncSession = Depends(get_session)) -> list[BeverageOut]:
    return await BeverageService.get_all_beverages(session)


@router.delete("/delete_by_id/{beverage_id}", status_code=status.HTTP_200_OK)
async def delete_beverage_by_id(
    beverage_id: int,
    session: AsyncSession = Depends(get_session),
):
    return await BeverageService.delete_beverage_by_id(beverage_id, session)

