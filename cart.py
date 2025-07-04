from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.schemas import CartCreate

router = APIRouter(prefix="/cart", tags=["cart"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_all_cart_items(db: Session = Depends(get_db)):
    return db.execute("SELECT * FROM cart").fetchall()

@router.get("/{cart_id}")
def get_cart_item(cart_id: int, db: Session = Depends(get_db)):
    cart = db.execute("SELECT * FROM cart WHERE cart_id = %s", (cart_id,)).fetchone()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return cart

@router.post("/")
def add_to_cart(cart: CartCreate, db: Session = Depends(get_db)):
    db.execute("""
        INSERT INTO cart (user_id, product_id, quantity) VALUES (%s, %s, %s)
    """, (cart.user_id, cart.product_id, cart.quantity))
    db.commit()
    return {"msg": "Cart item deleted"}
