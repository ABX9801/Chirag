from pydantic import BaseModel, Field
from datetime import datetime

class ChatDocument(BaseModel):
    username : str = Field(...)
    user_input : str = Field(...)
    reply : str = Field(...)
    created_at : datetime = Field(default=datetime.utcnow())