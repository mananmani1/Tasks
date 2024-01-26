
from database.models import *
from database.connection import SessionLocal
from sqlalchemy.orm import Session
from fastapi import FastAPI
from database.schemas import *

class ConversationRoutes():
   """Inherits from Routable."""

   def __init__(self) -> None:
       super().__init__()

   def get_db(self):
       db = SessionLocal()
       try:
           yield db
       finally:
           db.close()



