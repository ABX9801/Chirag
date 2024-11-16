import jwt
from config import JWT_SECRET_KEY, JWT_ALGORITHM
from app.db.mongodb import MongoClient, get_database_conn
from app.services.user import find_user_by_username
from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.models.user import User


security = HTTPBearer()
def _get_authorisation_token(authorisation: HTTPAuthorizationCredentials=Security(security)):
    print(authorisation)
    if authorisation.scheme != "Bearer":
        raise HTTPException(
            status_code=403, detail="Not authenticated"
        )
    
async def authorise_user_by_token(
        token : str = Depends(_get_authorisation_token), 
        dbclient : MongoClient = Depends(get_database_conn)
):
    try:
        user = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username = user["username"]
        password = user["password"]
        user = await find_user_by_username(username, dbclient)
        user_obj = User(**user)
        if user and user_obj.verify_password(password):
            return user_obj
        else:
            return None
    except Exception as err:
        print(f"Error authorising user || {err}")
        return None