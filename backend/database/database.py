from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

import os
from dotenv import loed_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")

DB_USERS_NAME = os.getenv("DB_USERS_NAME")
DB_POSTS_NAME = os.getenv("DB_POSTS_NAME")
DB_COMMENTS_NAME = os.getenv("DB_COMMENTS_NAME")

USERS_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_USERS_NAME}"
POSTS_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_POSTS_NAME}"
COMMENTS_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_COMMENTS_NAME}"

users_engine = create_engine( USERS_DATABASE_URL )

posts_engine = create_engine( POSTS_DATABASE_URL )

comments_engine = create_engine( COMMENTS_DATABASE_URL )

UsersSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=users_engine)

PostsSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=posts_engine)

CommentsSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=comments_engine)

Base = declarative_base()

def get_users_db():
    users_db = UsersSessionLocal()
    try:
        yield users_db
    finally:
        users_db.close()

def get_posts_db():
    posts_db = PostsSessionLocal()
    try:
        yield posts_db
    finally:
        posts_db.close()

def get_comments_db():
    comments_db = CommentsSessionLocal()
    try:
        yield comments_db
    finally:
        comments_db.close()
