from app.db.mongodb import MongoClient
from config import USER_COLLECTION, DB_NAME, JWT_SECRET_KEY, JWT_ALGORITHM
import bcrypt
import jwt
from app.models.user import UserToCreate, User, UserResponse


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