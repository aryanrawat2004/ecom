from fastapi import FastAPI
from routes import user, admin, product, cart

from auth import routes as auth_routes

app = FastAPI()

app.include_router(user.router)
app.include_router(admin.router)
app.include_router(product.router)
app.include_router(cart.router)

@app.get("/")
def home():
    return {"msg": "E-commerce API is running"}
