from app.models.user import User
from app.models.ChatResponse import ChatResponseStr, Emotions, UserContext
from app.db.mongodb import MongoClient
from app.chatbot.GirlBot import GirlBot
from config import DB_NAME, USER_COLLECTION

async def update_user_context(user: User, dbclient : MongoClient):
    try:
        await dbclient[DB_NAME][USER_COLLECTION].update_one(
            {"username" : user.username}, 
            {"$set" : user.dict()}
        )
    except Exception as err:
        print("Error in updating user context || ", err)

async def chat_with_girlbot(user: User, input : str, dbclient : MongoClient)-> ChatResponseStr:
    try:
        bot = GirlBot()
        bot.update_user_context(user.user_context.dict())
        bot.store_user_emotion(user.user_emotions.dict())
        response = bot.chat(input)
        user.user_context = UserContext(**bot.user_context)
        user.user_emotions = Emotions(**bot.user_emotion)
        await update_user_context(user, dbclient)
        return ChatResponseStr(response=response)
    except Exception as err:
        print("Error in Chatting to User || ", err)
        return ChatResponseStr(response="I'm having some trouble please try after sometime.")
    
