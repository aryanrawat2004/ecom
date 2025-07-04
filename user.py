from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import SessionLocal
from typing import List
from models.schemas import UserCreate

router = APIRouter(prefix="/users", tags=["users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_all_users(db: Session = Depends(get_db)):
    users = db.execute("SELECT * FROM user").fetchall()
    return users

@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.execute("SELECT * FROM user WHERE user_id = %s", (user_id,)).fetchone()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}")
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db.execute("""
        UPDATE user SET first_name=%s, last_name=%s, email=%s, phone_no=%s, date_of_birth=%s 
        WHERE user_id=%s
    """, (user.first_name, user.last_name, user.email, user.phone_no, user.date_of_birth, user_id))
    db.commit()
    return {"msg": "User updated"}

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db.execute("DELETE FROM user WHERE user_id=%s", (user_id,))
    db.commit()
    return {"msg": "User deleted"}
