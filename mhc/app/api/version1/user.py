from fastapi import APIRouter, Body, Depends

from app.utils.jwt import authorise_user_by_token

from ...db.mongodb import get_database_conn, MongoClient
from ...models.user import User, UserToCreate, UserResponse
from ...services.user import create_user_in_db, get_google_calendar_access_token, log_user_in

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


## Login User
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
    

## Get User Calendar Access Token
@router.post("/user/calendar/access", response_model=dict)
async def get_user_calendar_access_token(
    db : MongoClient = Depends(get_database_conn),
    user : User = Depends(authorise_user_by_token),
    calendar_code : str = Body(..., embed=True)
):
    try:
        if user:
            acess_token = await get_google_calendar_access_token(user, db, calendar_code)
            return {"access_token" : acess_token}
        else:
            return {"access_token" : ""}
    except Exception as err:
        print(f"Error getting user calendar access token || {err}")
        return {"access_token" : ""}