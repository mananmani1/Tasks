
from database.models import *
from database.connection import SessionLocal
from sqlalchemy.orm import Session
from fastapi import FastAPI
from database.schemas import *

class ConversationRoutes():

   def get_db(self):
       db = SessionLocal()
       try:
           yield db
       finally:
           db.close()



