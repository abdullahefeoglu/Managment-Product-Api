import decimal
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import create_table


app = FastAPI()
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
def get_products():
    return products

@app.get("/products/{product_id}")
def get_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return product


    raise HTTPException(
        status_code=404,
        detail="Product not found"
    )

@app.post("/products", status_code=201)
def create_product(product: Product):
    new_id = max(p["id"] for p in products) + 1

    new_product = {
        "id" : new_id,
        "name" : product.name,
        "price" : product.price
    }

    products.append(new_product)

    return new_product

@app.put("/products/{product_id}")
def update_product(product_id: int, updated_product: Product):
    for product in products:
        if product["id"] == product_id:
            product["name"] = updated_product.name
            product["price"] = updated_product.price
            return product

    raise HTTPException(
        status_code=404,
        detail="Product not found"
    )


@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    for index, product in enumerate(products):
        if product["id"] == product_id:
            deleted_product = products.pop(index)
            return {
                "message": "Product deleted successfully",
                "product": deleted_product
            }

    raise HTTPException(
        status_code=404,
        detail="Product not found"
    )
