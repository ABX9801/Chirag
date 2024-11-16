from pydantic import BaseModel, Field

class Emotions(BaseModel):
    Happiness: float = Field(default=0.0)
    Sadness: float = Field(default=0.0)
    Fear: float = Field(default=0.0)
    Anger: float = Field(default=0.0)
    Surprise: float = Field(default=0.0)
    Disgust: float = Field(default=0.0)
    Contempt: float = Field(default=0.0)
    Anticipation: float = Field(default=0.0)
    Suicidality: float = Field(default=0.0)

class UserContext(BaseModel):
    name: str = Field(default=None)
    age: str = Field(default=None)
    context: str = Field(default=None)


class ChatResponse(BaseModel):
    user: UserContext = Field(default=UserContext())
    emotions: Emotions = Field(default=Emotions())
    response: str = Field(default=None)

class ChatResponseStr(BaseModel):
    response : str = Field(default="I'm having some trouble atm, Please try later")