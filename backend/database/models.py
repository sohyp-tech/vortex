from database.database import Base
from sqlalchemy import Column, String, Float, Integer, DateTime
import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30))
    age = Column(Float)
    password = Column(String(35), unique=True)

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    poster = Column(String(30))
    content = Column(String(400))
    date = Column(DateTime, datetime.datetime.utcnow(), nullable = False)

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    commenter = Column(String)
    comment = Column(String(200))
    date = Column(DateTime, datetime.datetime.utcnow(), nullable = False)