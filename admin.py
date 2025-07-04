from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.schemas import UserCreate

router = APIRouter(prefix="/admins", tags=["admins"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_all_admins(db: Session = Depends(get_db)):
    return db.execute("SELECT * FROM admin").fetchall()

@router.get("/{admin_id}")
def get_admin(admin_id: int, db: Session = Depends(get_db)):
    admin = db.execute("SELECT * FROM admin WHERE admin_id = %s", (admin_id,)).fetchone()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    return admin

@router.put("/{admin_id}")
def update_admin(admin_id: int, admin: UserCreate, db: Session = Depends(get_db)):
    db.execute("""
        UPDATE admin SET first_name=%s, last_name=%s, email=%s, phone_no=%s, date_of_birth=%s 
        WHERE admin_id=%s
    """, (admin.first_name, admin.last_name, admin.email, admin.phone_no, admin.date_of_birth, admin_id))
    db.commit()
    return {"msg": "Admin updated"}

@router.delete("/{admin_id}")
def delete_admin(admin_id: int, db: Session = Depends(get_db)):
    db.execute("DELETE FROM admin WHERE admin_id=%s", (admin_id,))
    db.commit()
    return {"msg": "Admin deleted"}
