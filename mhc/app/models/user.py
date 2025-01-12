from pydantic import BaseModel, Field, EmailStr
from passlib.context import CryptContext
from typing import Optional
from app.models.ChatResponse import UserContext, Emotions

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserToCreate(BaseModel):
    username: str = Field(default=None)
    password: str = Field(default=None)
    email: EmailStr = Field(default=None)

class UserLocation(BaseModel):
    latitude : float = Field(default=None)
    longitude : float = Field(default=None)

class User(BaseModel):
    username: str = Field(default=None)
    hashedPassword: str = Field(default=None)
    email: EmailStr = Field(default=None)
    salt : str = Field(default=None)
    user_context : UserContext = Field(default=UserContext())
    conversation_context : str = Field(default="")
    google_calendar_access_token : Optional[str] = Field(default=None)
    google_calendar_refresh_token : Optional[str] = Field(default=None)
    user_location : UserLocation = Field(default=UserLocation())

    def verify_password(self, password):
        return password_context.verify(password, self.hashedPassword)


class UserResponse(BaseModel):
    username: str = Field(...)
    email: EmailStr = Field(...)
    token: str = Field(...)