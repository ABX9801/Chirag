import dotenv
import os

dotenv.load_dotenv('.env')

## CONN STRINGS
MONGODB_URL  = os.getenv("MONGODB_URL")

#DATABASE NAME
DB_NAME = os.getenv("DB_NAME")

## COLLECTIONS
USER_COLLECTION = "users"
CHATS_COLLECTION =  "chats"

## SECTETS/KEYS
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")