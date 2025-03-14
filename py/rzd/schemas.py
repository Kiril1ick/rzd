import datetime
from pydantic import BaseModel


class User(BaseModel):
        id: int
        name: str


class User_Work_sessions(BaseModel):
        date_id: int
        user_id: int
        work_hour: int

class Work_session(BaseModel):
        ws_id: int
        day: datetime.datetime
