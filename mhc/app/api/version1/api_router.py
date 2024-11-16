from fastapi import APIRouter
from app.api.version1.user import router as user_router
from app.api.version1.chat import router as chat_router

router = APIRouter()

router.include_router(user_router)
router.include_router(chat_router)