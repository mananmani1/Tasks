from sqlalchemy import Column, Integer, String, Enum, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, UniqueConstraint, CheckConstraint, text
from enum import Enum as PyEnum
import enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.dialects.mysql import VARCHAR

Base = declarative_base()


class DataSet(Base):
    __tablename__ = 'dataset'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    extracted_data = Column(JSON, nullable=False)

