import sqlite3

def get_connection():
    connection = sqlite3.connect("products.db")
    connection.row_factory = sqlite3.Row
    return connection

def create_table():
    connection = get_connection()
    connection.execute("""
    CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL )
    """)

    connection.commit()
    connection.close()

def get_products():
    connection = get_connection()
    products = connection.execute(
        "SELECT * FROM products"
    ).fetchall()

    connection.close()
    return [dict(product) for product in products]

def add_product(name, price):
    connection = get_connection()
    connection.execute(
        "INSERT INTO products (name, price) VALUES (?, ?)", (name,price)
    )

    connection.commit()
    connection.close()


def get_product(product_id):
    connection = get_connection()

    product = connection.execute(
        "SELECT * FROM products WHERE id = ?", (product_id,)
    ).fetchone()

    connection.close()
    return dict(product) if product else None

def update_product(product_id,name,price):
    connection = get_connection()
    cursor = connection.execute(
        "UPDATE products SET name = ?, price = ? WHERE id = ?",(name,price,product_id)
    )

    connection.commit()
    updated = cursor.rowcount > 0
    connection.close()
    return updated


def delete_product(product_id):
    connection = get_connection()
    cursor = connection.execute(
        "DELETE FROM products WHERE id = ?",(product_id,)
    )

    connection.commit()
    deleted = cursor.rowcount > 0
    connection.close()
    return deleted