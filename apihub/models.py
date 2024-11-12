from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class OllamaModel(Base):
    __tablename__ = 'OllamaModelTable'
    id = Column(Integer, primary_key=True, autoincrement=True)
    at_create = Column(DateTime, default=datetime.utcnow, nullable=False)
    at_update = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    name = Column(String, nullable=False)

class TaskModel(Base):
    __tablename__ = 'TaskTable'
    id = Column(Integer, primary_key=True, autoincrement=True)
    at_create = Column(DateTime, default=datetime.utcnow, nullable=False)
    at_update = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    name = Column(String, nullable=False)
    task = Column(String, nullable=False)
    response = Column(String, nullable=False)
    done = Column(Boolean, default=False, nullable=False)