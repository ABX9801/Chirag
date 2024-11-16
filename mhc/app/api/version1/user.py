from fastapi import APIRouter, Body, Depends

from ...utils.jwt import authorise_user_by_token
from ...db.mongodb import get_database_conn, MongoClient
from ...models.user import User, UserToCreate, UserResponse
from ...services.user import create_user_in_db, log_user_in

router = APIRouter()

## Create User
@router.post("/user/create", response_model=UserResponse)
async def create_user(
    user_create : UserToCreate = Body(..., embed=True),
    db : MongoClient = Depends(get_database_conn)
):
    try:
        user_res = await create_user_in_db(user_create, db)
        return user_res
    except Exception as err:
        print(f"Error creating user || {err}")
        return UserResponse(username = "ERROR", email = "error@email.com", token="")
    
@router.post("/user/login", response_model=UserResponse)
async def login_user(
    user_create : UserToCreate = Body(..., embed=True),
    db : MongoClient = Depends(get_database_conn)
):
    try:
        user_res = await log_user_in(user_create, db)
        return user_res
    except Exception as err:
        print(f"Error logging in user || {err}")
        return UserResponse(username = "ERROR", email = "error@email.com", token="")