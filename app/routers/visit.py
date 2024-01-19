from fastapi import APIRouter, Depends, status, Query
# from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession
import datetime
from app.db import get_session
from app.schemas.visit import VisitChange, VisitIn, VisitOut
from app.services.visit import VisitService

router = APIRouter(tags=["Visit"], prefix="/visit")


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_visit(
    visit_data: VisitIn,
    session: AsyncSession = Depends(get_session),
):
    return await VisitService.create_visit(visit_data, session)


@router.get("/get_by_id/{visit_id}", status_code=status.HTTP_200_OK)
async def get_visit_by_id(
    visit_id: int,
    session: AsyncSession = Depends(get_session),
) -> VisitOut:
    return await VisitService.get_visits_by_id(visit_id, session)


@router.get("/get_all", status_code=status.HTTP_200_OK)
async def get_all_visits(
    start: datetime.date ,
    end: datetime.date ,
    session: AsyncSession = Depends(get_session),  limit: int = Query(100, ge=0),
        offset: int = Query(0, ge=0),):
    
    return await VisitService.get_all_visits(session, limit, offset, start, end)


@router.post(
    "/update_visit",
    status_code=status.HTTP_200_OK
)
async def update_visit(
    visit_data: VisitChange,
    session: AsyncSession = Depends(get_session),
):
    return await VisitService.update_visit(visit_data, session)




