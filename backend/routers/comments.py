from fastapi import APIRouter, Depends, HTTPException
from database.database import comments_engine, get_comments_db, Base
from database.models import Comment
from database.schema import CommentCreate
from sqlalchemy.orm import Session
import database.models
import datetime

router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)

Base.metadata.create_all(bind=comments_engine)


@router.post("/add_comment")
def add_comment(comment_validate: CommentCreate, db: Session = Depends(get_comments_db)):

    try:
        new_comment = Comment (
            commenter = comment_validate.commenter_name,
            comment = comment_validate.comment_content
        )
        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)
        return {
            "status": "200",
            "added_status": "successfully!"
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code = 500, detail = str(e))


@router.get("/get_comments")
def get_comments(db: Session = Depends(get_comments_db)):

    try:
        comments = db.query(Comment).all()
        if comments:
            comments_list = []
            for comment in comments:
                comments_list.append({
                    "comment_id": comment.id,
                    "commenter_name": comment.commenter,
                    "comment_content": comment.comment,
                    "comment_date": comment.date
                })
            return {
                "status": "200",
                "comments": comments_list
            }
        else:
            return {
                "comments": "No Comments Found."
            }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))


@router.put("/edit_comment/{commenter_name}/{comment_id}")
def edit_comment(commenter_name: str, comment_id: int, new_content: str, db: Session = Depends(get_comments_db)):
    
    try:
        user_comment = db.query(Comment).filter(Comment.commenter == commenter_name, Comment.id == comment_id).first()
        if user_comment:
            user_comment.comment = new_content
            db.commit()
            db.refresh(user_comment)
            return {
                "status": "200",
                "commenter": commenter_name,
                "new_comment": user_comment.comment
            }
        else:
            raise HTTPException(status_code=404, detail="Comment not found or unauthorized")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))


@router.delete("/remove_comment/{commenter_name}/{comment_id}")
def remove_comment(commenter_name: str, comment_id: int, db: Session = Depends(get_comments_db)):
    
    try:
        user_comment = db.query(Comment).filter(Comment.commenter == commenter_name, Comment.id == comment_id).first()
        if user_comment:
            db.delete(user_comment)
            db.commit()
            return {
                "status": "200",
                "commenter": commenter_name,
                "comment": "comment deleted successfully!"
            }
        else:
            raise HTTPException(status_code=404, detail="Comment not found or unauthorized")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))