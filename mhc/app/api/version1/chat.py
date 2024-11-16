from fastapi import APIRouter, Body, Depends, HTTPException
from app.models.user import User
from app.services.chat import chat_with_girlbot
from ...models.ChatResponse import ChatResponseStr
from ...utils.jwt import authorise_user_by_token
from ...db.mongodb import get_database_conn, MongoClient

router = APIRouter()

@router.post("/chat", response_model=ChatResponseStr)
async def chat(
    chat_input : str  = Body(..., embed=True),
    db : MongoClient = Depends(get_database_conn),
    user : User = Depends(authorise_user_by_token)
):
    if user:
        return await chat_with_girlbot(user, chat_input, db)
    else:
        raise HTTPException(status_code=422, detail="Invalid credentials")