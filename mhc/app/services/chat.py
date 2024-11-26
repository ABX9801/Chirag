import asyncio
from app.models.user import User
from app.models.ChatResponse import ChatResponseStr, Emotions, UserContext
from app.db.mongodb import MongoClient
from app.chatbot.GirlBot import GirlBot
from config import DB_NAME, USER_COLLECTION, CHATS_COLLECTION
from app.models.chat import ChatDocument


async def update_user_context(dbclient : MongoClient, user: User, user_info: dict, conversation_context: str):
    try:
        await dbclient[DB_NAME][USER_COLLECTION].update_one(
            {"username" : user.username}, 
            {
                "$set" : {
                    "user_context" : user_info,
                    "conversation_context" : conversation_context
                }
            }
        )
    except Exception as err:
        print("Error in updating user context || ", err)


async def get_previous_chats_for_user(user: User, dbclient : MongoClient):
    try:
        previous_chats = await dbclient[DB_NAME][CHATS_COLLECTION].find(
            {
                "username" : user.username
            },
            {
                "user_input" : 1,
                "reply" : 1
            },
            sort = [("created_at", -1)],
        ).limit(5).to_list(None)
        return previous_chats
    except Exception as err:
        print("Error in getting previous chats || ", err)
        return []


async def save_user_chat(user: User, input : str, reply : str, dbclient : MongoClient):
    try:
        chat_doc = ChatDocument(**{
            "username" : user.username,
            "user_input" : input,
            "reply" : reply
        }).dict()
        await dbclient[DB_NAME][CHATS_COLLECTION].insert_one(chat_doc)
    except Exception as err:
        print("Error in saving user chat || ", err)


async def chat_with_girlbot(user: User, input : str, dbclient : MongoClient)-> ChatResponseStr:
    try:
        bot = GirlBot()
        previous_chats = await get_previous_chats_for_user(user, dbclient)
        bot.previous_conversation = previous_chats
        bot.conversation_context = user.conversation_context
        bot.user_context = user.user_context
        response = bot.chat(input)
        await asyncio.gather(
            update_user_context(dbclient, user, bot.user_context, bot.conversation_context),
            save_user_chat(user, input, response, dbclient)
        )
        return ChatResponseStr(response=response)
    except Exception as err:
        print("Error in Chatting to User || ", err)
        return ChatResponseStr(response="I'm having some trouble please try after sometime.")
    
