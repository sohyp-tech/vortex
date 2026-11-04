from fastapi import APIRouter, Depends, HTTPException
from database.database import posts_engine , get_posts_db, Base
from database.models import Post
from database.schema import PostCreate
from sqlalchemy.orm import Session
import database.models
import datetime

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

Base.metadata.create_all(bind=posts_engine)

@router.post("/add_post")
def add_post(post_validate: PostCreate, db: Session = Depends(get_posts_db)):

    try:
        new_post = Post (
            poster = post_validate.poster_name,
            content = post_validate.post_content
        )
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return {
            "status": "200",
            "added_status": "successfully!"
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code = 500, detail = str(e))


@router.get("/get_posts")
def get_posts(db: Session = Depends(get_posts_db)):

    try:
        posts = db.query(Post).all()
        if posts:
            posts_list = []
            for post in posts:
                posts_list.append({
                    "poster_id": post.id
                    "poster_name": post.poster,
                    "post_content": post.content,
                    "post_date": post.date
                })
            return {
                "status": "200",
                "posts": posts_list
            }
        else:
            return {
                "posts": "No Posts Found."
            }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))


@router.get("/get_user_posts/{poster_name}")
def get_user_posts(poster_name: str, db: Session = Depends(get_posts_db)):
    
    try:
        user_posts = db.query(Post).filter(Post.poster == poster_name).all()
        if user_posts:
            posts_list = []
            for post in user_posts:
                posts_list.append({
                    "poster_id": post.id,
                    "post_content": post.content,
                    "post_date": post.date
                })
            return {
                "status": "200",
                "poster_name": poster_name,
                "posts": posts_list
            }
        else:
            return {
                "posts": "No Posts Found."
            }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))


@router.put("/edit_post/{poster_name}/{post_id}")
def edit_post(poster_name: str, post_id: int, new_content: str, db: Session = Depends(get_posts_db)):
    
    try:
        user_post = db.query(Post).filter(Post.poster == poster_name, Post.id == post_id).first()
        if user_post:
            user_post.content = new_content
            db.commit()
            db.refresh(user_post)
            return {
                "status": "200",
                "poster": poster_name
                "new_post": user_post.content
            }
        else:
            db.rollback()
            raise HTTPException(status_code=404, detail="user not found")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))


@router.put("/remove_post/{poster_name}/{post_id}")
def remove_post(poster_name: str, post_id: int, new_content: str, db: Session = Depends(get_posts_db)):
    
    try:
        user_post = db.query(Post).filter(Post.poster == poster_name, Post.id == post_id).first()
        if user_post:
            db.delete(user_post)
            db.commit()
            return {
                "status": "200",
                "poster": poster_name
                "post": "post deleted successfully!"
            }
        else:
            raise HTTPException(status_code=404, detail="user not found")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))

