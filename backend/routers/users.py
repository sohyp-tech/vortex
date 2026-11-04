from fastapi import APIRouter, Depends, HTTPException, Query
from database.database import users_engine , get_users_db, Base
from database.models import User
from database.schema import UserCreate
from sqlalchemy.orm import Session
import database.models
from typing import Any
from passlib.context import CryptContext

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

Base.metadata.create_all(bind=users_engine)

@router.post("/add_user")
def add_user(user_validate: UserCreate, db: Session = Depends(get_users_db)):
    
    try:
        new_user = User (
            name = user_validate.user_name,
            age = user_validate.user_age,
            password = pwd_context.hash(user_validate.user_password)
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {
            "status": "user added successfully 200!"
        }

    except Exception as e:
        db.rollback()
        if not user_validate:
            raise HTTPException(status_code=401, detail=str(e))
        else:
            raise HTTPException(status_code=500, detail=str(e))


@router.get("/get_user/{name}/{age}")
def get_user(name: str, age: float, db: Session = Depends(get_users_db)):

    try:
        user = db.query(User).filter(User.name == name, User.age == age).first()
        if user:
            return {
                "user_name": user.name,
                "user_age": user.age
            }
        else:
            raise HTTPException(status_code=404, detail=f"User {name} not found.")
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/update_user/{user_name}/{user_password}/update_age/{new_age}/update_name/{new_name}")
def update_user(user_name: str, new_age: float,user_password: str, new_name: str, db: Session = Depends(get_users_db)):

    try:
        user = db.query(User).filter(User.name == user_name).first()
        if not user:
            raise HTTPException(status_code=404, detail=f"404, User {user_name} not found.")
        else:
            isCorrectPass = pwd_context.verify(user_password, user.password)
            if isCorrectPass:
                user.name = new_name
                user.age = new_age
                db.commit()
                db.refresh(user)
                return { "status": f"200 user {user_name} updated to {new_name}" }
            else:
                raise HTTPException(status_code=401, detail="Invalid Data.")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete_user/{user_name}/{user_age}")
def delete_user(user_name: str, user_age: float, password: str = Query(...) , db: Session = Depends(get_users_db)):

    try:
        user = db.query(User).filter(User.name == user_name, User.age == user_age).first()
        if not user:
            raise HTTPException(status_code=404, detail=f"User {user_name} not found.")
        else:
            isCorrectPass = pwd_context.verify(password, user.password)
            if isCorrectPass:
                db.delete(user)
                db.commit()
                return { "status": f"200, User {user_name} deleted successfully" }
            else:
                db.rollback()
                raise HTTPException(status_code=401, detail="Invalid Data.")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
