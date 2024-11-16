from pydantic import BaseModel, Field, EmailStr
from passlib.context import CryptContext

from app.models.ChatResponse import UserContext, Emotions

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserToCreate(BaseModel):
    username: str = Field(default=None)
    password: str = Field(default=None)
    email: EmailStr = Field(default=None)


class User(BaseModel):
    username: str = Field(default=None)
    hashedPassword: str = Field(default=None)
    email: EmailStr = Field(default=None)
    salt : str = Field(default=None)
    user_context : UserContext = Field(default=UserContext())
    user_emotions : Emotions = Field(default=Emotions())

    def verify_password(self, password):
        return password_context.verify(password, self.hashedPassword)


class UserResponse(BaseModel):
    username: str = Field(...)
    email: EmailStr = Field(...)
    token: str = Field(...)