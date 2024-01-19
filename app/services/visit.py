from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse

from jose import JWTError, jwt
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
import datetime
from app.daos import bar
from app.daos import visit
from app.daos import stock
from app.db import get_session
from app.models.visit import Visit as VisitModel
from app.schemas.visit import VisitChange, VisitIn, VisitBase, VisitOut

class VisitService:
    @staticmethod
    async def create_visit(visit_data: VisitIn, session: AsyncSession):
        visit_model = {
            "visitedOn" : visit_data.visitedOn,
            "bar_id": visit_data.bar_id
        }
    
        new_visit = await visit.VisitDao(session).create(visit_model)

        if new_visit:
            create_drink = {
             "happy_hour": visit_data.happy_hour,
             "visit_id" : new_visit.visit_id,
             "stock_id" : visit_data.stock_id,
             "quantity": visit_data.quantity
            }
            print(create_drink)
            drink = await visit.VisitDao(session).create_drink(create_drink)            
            logger.info(f"New drink created successfully: {drink}!!!")

        logger.info(f"New visit created successfully: {new_visit}!!!")
        return JSONResponse(
            content={"message": "Visit created successfully"},
            status_code=status.HTTP_201_CREATED,
        )

    @staticmethod
    async def get_all_visits(session: AsyncSession, limit: int, offset: int, start: datetime.date, end: datetime.date) -> list[VisitOut]:
        all_visits = await visit.VisitDao(session).get_all(limit, offset, start, end)
        visit_data = []
        for visit_ in all_visits:
            bar_ = await bar.BarDao(session).get_by_id(visit_.bar_id)
            drink_ = await visit.VisitDao(session).get_drink_by_visit_id(visit_.visit_id)

            beverage = await stock.StockDao(session).get_by_id(drink_.stock_id) 


            visit_data.append({
                "visit_id": visit_.visit_id,
                "drinks" : drink_.quantity,
                "happy_hour": drink_.happy_hour,
                "bar_name" : bar_.name,
                "beverage": beverage.name,
                "visitedOn" : visit_.visitedOn
            })

        return visit_data


    @staticmethod
    async def get_visits_by_id(visit_id: int, session: AsyncSession) -> VisitOut:
        _visit = await visit.VisitDao(session).get_by_id(visit_id)
        if not _visit:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Visit with the given id does not exist!!!",
            )
        
        bar_ = await bar.BarDao(session).get_by_id(_visit.bar_id)
        if not bar_:
             raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No bars on visit",
            )

        drink_ = await visit.VisitDao(session).get_drink_by_visit_id(_visit.visit_id)

        if not drink_:
            logger.info("")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No drinks found",
            )
        beverage = await stock.StockDao(session).get_by_id(drink_.stock_id) 

        visit_data= {
                "visit_id": _visit.visit_id,
                "drinks" : drink_.quantity,
                "happy_hour": drink_.happy_hour,
                "bar_name" : bar_.name,
                "beverage": beverage.name,
                "visitedOn" : _visit.visitedOn
            }
        return visit_data 
    


    @staticmethod
    async def update_visit(
        visit_data: VisitChange,
        session: AsyncSession = Depends(get_session),
    ):
        _drink = await visit.VisitDao(session).get_drink_by_visit_id(visit_data.visit_id) 
        _visit = await visit.VisitDao(session).get_by_id(visit_data.visit_id)
        if not _visit and not _drink:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Data given does not does not exist!!!",
            )
        #Updating visits data
        _visit.visitedOn = visit_data.visitedOn
        _visit.bar_id = visit_data.bar_id
        session.add(_visit)
       
       # Updating drinks taken
        _drink.happy_hour = visit_data.happy_hour
        _drink.quantity = visit_data.quantity
        _drink.stock_id = visit_data.stock_id
        session.add(_visit)

        await session.commit()
        return JSONResponse(
            content={"message": "Visit updated successfully!!!"},
            status_code=status.HTTP_200_OK,
        )

 