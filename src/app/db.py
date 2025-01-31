import os

from sqlalchemy import (Column, Integer, String, Table, create_engine, MetaData)
from dotenv import load_dotenv
from databases import Database
from datetime import datetime as dt
from pytz import timezone as tz
from pydantic import BaseModel


load_dotenv()
# Database url if none is passed the default one is used
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://hello_fastapi:hello_fastapi@localhost/hello_fastapi_dev")

# SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata = MetaData()
notes = Table(
    "notes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(50)),
    Column("description", String(50)),
    Column("completed",String(8), default="False"),
    Column("created_date", String(50), default=dt.now(tz("Africa/Nairobi")).strftime("%Y-%m-%d %H:%M"))
)
# # Databases query builder

database = Database(DATABASE_URL)

class NoteSchema(BaseModel):
    title: str
    description: str
    completed: bool

class NoteDB(NoteSchema):
    id: int
    created_date: str

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "My first note",
                "description": "This is my first note",
                "completed": False,
                "created_date": "2021-07-01 00:00:00"
            }
        }