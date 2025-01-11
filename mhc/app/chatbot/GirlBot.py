import json
from groq import Groq
from app.models.ChatResponse import CalendarInput, ChatResponse, Emotions, UserContext
from config import GROQ_API_KEY
from app.services.calendar import schedule_calendar_event_async
from  dateparser import parse
from datetime import datetime



class GirlBot:
    def __init__(self):
        self.groq = Groq(api_key=GROQ_API_KEY)
        self.user_context = UserContext().dict()
        self.conversation_context = ""
        self.previous_conversation = []
        self.user_email = ""

    def get_prompt(self, user_input: str):
        return f"""
        You are Aaradhya, a friendly and compassionate girl who is the user's friend. Your role is to support and empathize with the user while maintaining a positive and constructive tone. Below is some context about previous conversations and user information that you can refer to when crafting your response.
        Previous Conversations
        {self.previous_conversation}

        Conversation Context
        {self.conversation_context}

        Previous User Information
        {str(self.user_context)}

        User's Current Input
        {user_input}

        ### Todays Date
        {datetime.now().strftime("%Y-%m-%d")}

        Your Task
        Using the given information, respond as a supportive and understanding friend. Your response should be:
        1.Positive and constructive while acknowledging the user's emotions.
        2.Open-ended to encourage further conversation.
        3.Brief (20-30 words).
        4. If there is an ask for creating a calendar event for the user use the provided information create a json for the calendar event and return it. If there is no event to be created return an empty dictionary.
        If there is new information about the user, update the User Information accordingly. Additionally, refine the Conversation Context based on the new exchange to keep it concise (max 50 words).

        Response Format
        Provide your response strictly in JSON format:


        {str({
	        "user": {
		        "name": "User's Name",
		        "age": "User's Age Group (e.g., 0-5, 6-12, 13-18, etc.)"
	        },
	        "response": "A short and compassionate message tailored to the user (no more than 50 words, with or without emojis).",
	        "updated_context": "Updated context about the conversation in not more than 50 words.",
            "calenndar_event": str({
                "title": "Event Title",
                "start_datetime": "Event Start Date and TIme calculate from input in ISO Format",
                "end_datetime": "Event End Date and Time in ISO Format",
                "description": "a short description about the event"
            })
        })}

        """
    
    def chat_with_llm(self, user_input: str,):
        prompt = self.get_prompt(user_input)
        print("###########################################################################")
        print(prompt)
        print("###########################################################################")
        completion = self.groq.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[
                {
                    "role" : "system",
                    "content" : "You are Aradhya, a friendly and compassionate girl who is my friend."
                },
                {
                    "role" : "user",
                    "content" : prompt
                }
            ],
            temperature=0.1,
            max_tokens=1024,
            response_format={"type": "json_object"}
        )
        return completion
    

    def parse_response(self, chat_response) -> dict:
        try:
            response =  json.loads(chat_response.choices[0].message.content)
            response = ChatResponse(**response)
            return response.dict()
        except Exception as err:
            return {}
    

    def update_user_context(self, user_info: dict):
        print("Updating user context")
        self.user_context = user_info
        return self.user_context
    
    def update_conversation_context(self, conversation_context: str):
        print("Updating conversation context")
        self.conversation_context = conversation_context

    async def schedule_calendar_event(self, calendar_event: dict):
        try:
            calendar_event_obj = CalendarInput(**calendar_event)
            event = await schedule_calendar_event_async(
                user=self.user,
                summary=calendar_event_obj.title,
                description=calendar_event_obj.description,
                attendee_emails=[],
                start_date_time=calendar_event_obj.start_datetime,
                end_date_time=calendar_event_obj.end_datetime
            )
        except Exception as err:
            print("Error in scheduling calendar event || ", err)

    
    async def chat(self, user_input: str):
        chat_response = self.chat_with_llm(user_input)
        response = self.parse_response(chat_response)

        user_info = response.get("user")
        self.update_user_context(user_info)

        conversation_context = response.get("updated_context")
        self.update_conversation_context(conversation_context)
        
        calendar_event = response.get("calendar_event")
        if calendar_event:
            user_email = self.user_email
            await self.schedule_calendar_event(calendar_event)
        chat_response = response.get("response")
        return chat_response