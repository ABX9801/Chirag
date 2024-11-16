from app.models.user import User
from app.models.ChatResponse import ChatResponseStr, Emotions, UserContext
from app.db.mongodb import MongoClient
from app.chatbot.GirlBot import GirlBot

async def chat_with_girlbot(user: User, input : str, dbclient : MongoClient)-> ChatResponseStr:
    try:
        bot = GirlBot()
        user_context = UserContext(name="", age="", context="")
        bot.update_user_context(user_context.dict())
        response = bot.chat(input)
        return ChatResponseStr(response=response)
    except Exception as err:
        print("Error in Chatting to User || ", err)
        return ChatResponseStr(response="I'm having some trouble please try after sometime.")
    
