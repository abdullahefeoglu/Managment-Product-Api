import decimal
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import create_table
from  database import get_products, add_product,get_product as db_get_product,update_product,delete_product
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent

@app.get("/admin/add_product", include_in_schema=False)
def add_product_page():
    return FileResponse(BASE_DIR / "admin" / "add_product.html")


@app.get("/admin/delete_product", include_in_schema=False)
def delete_product_page():
    return FileResponse(BASE_DIR / "admin" / "delete_product.html")


@app.get("/admin/update_product", include_in_schema=False)
def update_product_page():
    return FileResponse(BASE_DIR / "admin" / "update_product.html")


@app.get("/user/list_product", include_in_schema=False)
def list_product_page():
    return FileResponse(BASE_DIR / "user" / "list_product.html")

create_table()

class Product(BaseModel):
    name:str
    price: float


products = [
    {"id": 1, "name": "Keyboard", "price": 1200},
    {"id": 2, "name": "Mouse", "price": 500},
    {"id": 3, "name": "Monitor", "price": 7500},
    {"id": 4, "name": "Computer", "price": 2000},
]



@app.get("/") #decorator
def home():
    return {"message" : "Product Management API is running"}

@app.get("/products")
def read_products():
    return get_products()

@app.get("/products/{product_id}")
def get_product(product_id: int):
    product = db_get_product(product_id)

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return product

@app.post("/products", status_code=201)
def create_product(product: Product):
    add_product(product.name, product.price)

    return {
        "message" : "Product created successfully",
        "name" : product.name,
        "price" : product.price
    }


@app.put("/products/{product_id}")
def edit_product(product_id: int, updated_product: Product):
    updated = update_product(
        product_id,
        updated_product.name,
        updated_product.price
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")

    return db_get_product(product_id)


@app.delete("/products/{product_id}")
def remove_product(product_id: int):
    deleted = delete_product(product_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")

