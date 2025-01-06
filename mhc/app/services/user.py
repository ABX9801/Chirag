from app.db.mongodb import MongoClient
from config import USER_COLLECTION, DB_NAME, JWT_SECRET_KEY, JWT_ALGORITHM
import bcrypt
import jwt
import json
import requests
from app.models.user import UserToCreate, User, UserResponse
import aiohttp


def get_token_for_user(user : UserToCreate):
    token = jwt.encode(user.dict(), JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token

    

async def log_user_in(user: UserToCreate, dbclient : MongoClient):
    try:
        user_in_db = await find_user_by_username(user.username, dbclient)
        if user_in_db is not None:
            user_obj = User(**user_in_db)
            if user_obj.verify_password(user.password):
                token = get_token_for_user(user)
                await get_google_calendar_access_token(user_obj, dbclient, "", grant_type="refresh_token")
                return UserResponse(**user_obj.dict(), token=token)
            else:
                return None
        else:
            return None
    except Exception as err:
        print(f"Error logging in user || {err}")
        return None



async def find_user_by_username(username : str, dbclient : MongoClient):
    try:
        user = await dbclient[DB_NAME][USER_COLLECTION].find_one({"username" : username})
        return user
    except Exception as err:
        print(f"Error finding user by username {username} || {err}")


async def create_user_in_db(user : UserToCreate, dbclient : MongoClient):
    try:
        user_in_db = await find_user_by_username(user.username, dbclient)
        if user_in_db:
            user_obj = User(**user_in_db)
            if user_obj.verify_password(user.password):
                print("User already Present")
                token = get_token_for_user(user)
                return  UserResponse(**user_in_db, token = token)
            else:
                return UserResponse(username = "ERROR", email = "error@email.com", token="")

        salt = bcrypt.gensalt()
        hashedPassword = bcrypt.hashpw(user.password.encode('utf-8'), salt)
        user_obj = User(
            username = user.username, 
            hashedPassword = hashedPassword, 
            email = user.email, 
            salt = salt
        )

        token = get_token_for_user(user)

        await dbclient[DB_NAME][USER_COLLECTION].insert_one(user_obj.dict())
        print("Created User In Collection")
        return UserResponse(**user_obj.dict(), token=token)
    except Exception as err:
        print(f"Error creating user || {err}")
        return UserResponse(username = "ERROR", email = "error@email.com", token="")
    

async def get_google_calendar_access_token(user: User, db: MongoClient, code : str, grant_type : str = "authorization_code"):
    try:
        with open('web_creds.json', 'r') as f:
            creds = json.load(f)
            client_id = creds['web']['client_id']
            client_secret = creds['web']['client_secret']
            app_redirect_uri = "http://localhost:3000/chatbot"
            token_endpoint = "https://oauth2.googleapis.com/token"
            if grant_type == "authorization_code":
                payload = {
                    'code': code,
                    'client_id': client_id,
                    'client_secret': client_secret,
                    'redirect_uri': app_redirect_uri,
                    'grant_type': grant_type
                }
                # Send the POST request
                async with aiohttp.ClientSession() as session:
                    async with session.post(token_endpoint, data=payload) as response:
                        if response.status == 200:
                            response_dict = await response.json()
                            access_token = response_dict['access_token']
                            refresh_token = response_dict.get('refresh_token')
                            # Save the access token and refresh token in the database
                            await db[DB_NAME][USER_COLLECTION].update_one(
                                {"username": user.username},
                                {
                                    "$set": {
                                        "google_calendar_access_token": access_token,
                                        "google_calendar_refresh_token": refresh_token
                                    }
                                }
                            )
                            return access_token
            elif grant_type == "refresh_token":
                refresh_token = user.google_calendar_refresh_token
                if refresh_token is None:
                    return None

                payload = {
                    'refresh_token': refresh_token,
                    'client_id': client_id,
                    'client_secret': client_secret,
                    'grant_type': grant_type
                }

                # Send the POST request
                async with aiohttp.ClientSession() as session:
                    async with session.post(token_endpoint, data=payload) as response:
                        if response.status == 200:
                            response_dict = await response.json()
                            access_token = response_dict['access_token']
                            refresh_token = response_dict.get('refresh_token')

                            # Save the access token and refresh token in the database
                            await db[DB_NAME][USER_COLLECTION].update_one(
                                {"username": user.username},
                                {
                                    "$set": {
                                        "google_calendar_access_token": access_token,
                                    }
                                }
                            )

                            return access_token
                        else:
                            return None        
    except Exception as err:
        print(f"Error obtaining Google Calendar access token || {err}")
        return None
                