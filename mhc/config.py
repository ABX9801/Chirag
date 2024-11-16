import dotenv
import os

dotenv.load_dotenv('.env')

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MONGODB_URL  = os.getenv("MONGODB_URL")