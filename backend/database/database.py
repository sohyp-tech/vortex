from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

USERS_DATABASE_URL = "sqlite:///./users.db"
POSTS_DATABASE_URL = "sqlite:///./posts.db"
COMMENTS_DATABASE_URL = "sqlite:///./comments.db"

users_engine = create_engine( USERS_DATABASE_URL, connect_args={ "check_same_thread": False} )

posts_engine = create_engine( POSTS_DATABASE_URL, connect_args={ "check_same_thread": False} )

comments_engine = create_engine( COMMENTS_DATABASE_URL, connect_args={ "check_same_thread": False} )

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