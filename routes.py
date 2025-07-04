from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import SessionLocal
from auth.jwt import create_access_token
from auth.utils import hash_password, verify_password
from models import schemas

router = APIRouter(prefix="/auth", tags=["auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed = hash_password(user.password)
    db.execute("INSERT INTO user (first_name, last_name, email, phone_no, date_of_birth) VALUES (%s, %s, %s, %s, %s)",
               (user.first_name, user.last_name, user.email, user.phone_no, user.date_of_birth))
    db.commit()
    return {"msg": "User created"}

@router.post("/login", response_model=schemas.Token)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    result = db.execute("SELECT * FROM user WHERE email = %s", (user.email,))
    db_user = result.fetchone()
    if not db_user or not verify_password(user.password, "hashed_password"):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
