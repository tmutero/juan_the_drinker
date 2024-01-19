from fastapi import APIRouter, Depends, status
# from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.schemas.token import Token
from app.schemas.bar import BarIn, BarOut, ChangeBarIn
from app.services.bar import BarService

router = APIRouter(tags=["Bar"], prefix="/bar")


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_bar(
    bar_data: BarIn,
    session: AsyncSession = Depends(get_session),
):
    return await BarService.create_bar(bar_data, session)


@router.get("/get_by_id/{bar_id}", status_code=status.HTTP_200_OK)
async def get_bar_by_id(
    bar_id: int,
    session: AsyncSession = Depends(get_session),
) -> BarOut:
    return await BarService.get_bar_by_id(bar_id, session)


@router.get("/get_all", status_code=status.HTTP_200_OK)
async def get_all_bars(session: AsyncSession = Depends(get_session)) -> list[BarOut]:
    return await BarService.get_all_bars(session)


@router.delete("/delete_by_id/{bar_id}", status_code=status.HTTP_200_OK)
async def delete_bar_by_id(
    bar_id: int,
    session: AsyncSession = Depends(get_session),
):
    return await BarService.delete_bar_by_id(bar_id, session)


@router.post(
    "/update_bar",
    status_code=status.HTTP_200_OK
)
async def update_bar(
    bar_data: ChangeBarIn,
    session: AsyncSession = Depends(get_session),
):
    return await BarService.update_bar(bar_data, session)

