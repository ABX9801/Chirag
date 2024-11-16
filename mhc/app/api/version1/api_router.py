from fastapi import APIRouter
from app.api.version1.user import router as user_router

router = APIRouter()

router.include_router(user_router)