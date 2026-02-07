from fastapi import APIRouter
from app.presentation.api.endpoints.home import router as home_router

router = APIRouter()

router.include_router(home_router)
