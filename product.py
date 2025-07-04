from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.schemas import ProductCreate

router = APIRouter(prefix="/products", tags=["products"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_all_products(db: Session = Depends(get_db)):
    return db.execute("SELECT * FROM product").fetchall()

@router.get("/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.execute("SELECT * FROM product WHERE Product_ID = %s", (product_id,)).fetchone()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/")
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db.execute("""
        INSERT INTO product (name, price, quantity, category)
        VALUES (%s, %s, %s, %s)
    """, (product.name, product.price, product.quantity, product.category))
    db.commit()
    return {"msg": "Product created"}

@router.put("/{product_id}")
def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    db.execute("""
        UPDATE product SET name=%s, price=%s, quantity=%s, category=%s WHERE Product_ID=%s
    """, (product.name, product.price, product.quantity, product.category, product_id))
    db.commit()
    return {"msg": "Product updated"}

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db.execute("DELETE FROM product WHERE Product_ID=%s", (product_id,))
    db.commit()
    return {"msg": "Product deleted"}
