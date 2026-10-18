from fastapi import FastAPI, HTTPException

app = FastAPI()

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