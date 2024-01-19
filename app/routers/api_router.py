from fastapi import APIRouter

from app.routers import user
from app.routers import stock
from app.routers import bar
from app.routers import beverage
from app.routers import visit

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(user.router)
api_router.include_router(bar.router)
api_router.include_router(stock.router)
api_router.include_router(beverage.router)
api_router.include_router(visit.router)

