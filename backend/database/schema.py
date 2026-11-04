from pydantic import BaseModel

class UserCreate(BaseModel):
    user_name: str
    user_age: float
    user_password: str

class PostCreate(BaseModel):
    poster_name: str
    post_content: str

class CommentCreate(BaseModel):
    commenter_name: str
    comment_content: str