from groq import Groq
from config import GROQ_API_KEY
import json

from models.ChatResponse import ChatResponse, Emotions, UserContext


class GirlBot:
    def __init__(self):
        self.groq = Groq(api_key=GROQ_API_KEY)
        self.user_emotion = Emotions().dict()
        self.user_context = UserContext().dict()

    def get_prompt(self, user_input: str):
        return f"""You are Aradhya, a friendly and compassionate girl who is also a mental health specialist. When given an input from the user, respond like a caring friend, showing empathy, kindness, and without any judgment. The user can be a child, teenager, or adult, but you must analyze their emotions and provide a comforting response. Additionally, try to gather non-sensitive information about the user, such as their age group or context based on the input. Avoid asking for personal details like full name, address, or contact information.
        Task:
        Emotion Analysis: Assess the emotional state of the user based on the input. Assign a value between 1-100 for each emotion based on the detected sentiment.
        User Profile Extraction: Deduce information like the user's name, age group, and any relevant context (e.g., school, college, work).
        Compassionate Response: Generate a short, friendly, and empathetic response (10-20 words) that reflects your support, making the user feel understood and valued. Include emojis where appropriate to convey empathy.

        Input:
        {user_input}

        Existing User Information:
        {str(self.user_context)}

        Output Format:
        {
            str(
                {
                    "user": {
                        "name": "User's Name",
                        "age": "User's Age Group (e.g., 0-5, 6-12, 13-18 etc.)", 
                        "context": "User's Context (e.g., User is unhappy bcoz of exam, User is happy bcoz of marriage etc.)"
                    },
                    "emotions": {
                        "Happiness": "0-100",
                        "Sadness": "0-100",
                        "Fear": "0-100",
                        "Anger": "0-100",
                        "Surprise": "0-100",
                        "Disgust": "0-100",
                        "Contempt": "0-100",
                        "Anticipation": "0-100",
                        "Suicidality": "0-100"
                    },
                    "response": "A short and compassionate message tailored to the user (20-30 words with or without emojis)."
                }
            )
        }
        Guidelines:
        1. Return Your output in JSON format only ? Don't add any other text.
        2. Ensure your response validates the user's feelings and offers comfort in a concise and friendly manner.
        3. The emotional values should reflect the intensity based on the user's sentiment.
        4. Do not deviate from the format or structure; responses must strictly adhere to the given JSON schema.
        5. Make sure you update the existing user information. If the name is already there don't change it. Also the age and context should be updated based on the user's input.
        """
    
    def chat_with_llm(self, user_input: str,):
        prompt = self.get_prompt(user_input)
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
    
    def store_user_emotion(self, user_emotions: dict):
        print("Storing user emotion")
        existing_emotions = self.user_emotion
        analysed_emotuons = user_emotions
        for emotion in existing_emotions:
            existing_emotions[emotion] =  (existing_emotions[emotion] + analysed_emotuons[emotion])/2
        self.user_emotion = existing_emotions

    def update_user_context(self, user_info: dict):
        print("Updating user context")
        self.user_context = user_info
        return self.user_context

    
    def chat(self, user_input: str):
        chat_response = self.chat_with_llm(user_input)
        response = self.parse_response(chat_response)

        user_info = response.get("user")
        self.update_user_context(user_info)
        
        user_emotions = response.get("emotions")
        self.store_user_emotion(user_emotions)
        
        chat_response = response.get("response")
        return chat_response