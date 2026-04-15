from fastapi import FastAPI
from datetime import datetime
import numpy as np
import pandas as pd

app = FastAPI()

#1,2
class User:
    def __init__(self, id: int, name: str, email: str):
        self._id = id
        self._name = name.strip().title()
        self._email = email.strip().lower()
        if "@" not in self._email:
            raise ValueError("Invalid email")

    def __str__(self):
        return f"User(id={self._id}, name='{self._name}', email='{self._email}')"

    def __del__(self):
        print(f"User {self._name} deleted")

    @classmethod
    def from_string(cls, data: str):
        parts = data.split(",")
        return cls(int(parts[0].strip()), parts[1].strip(), parts[2].strip())


#3
class Product:
    def __init__(self, id: int, name: str, price: float, category: str):
        self.id = id
        self.name = name
        self.price = price
        self.category = category

    def __str__(self):
        return f"Product(id={self.id}, name='{self.name}', price={self.price}, category='{self.category}')"

    def __eq__(self, other):
        return isinstance(other, Product) and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "price": self.price, "category": self.category}


#4,5
class Inventory:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        if product.id not in [p.id for p in self.products]:
            self.products.append(product)

    def remove_product(self, product_id):
        self.products = [p for p in self.products if p.id != product_id]

    def get_product(self, product_id):
        return next((p for p in self.products if p.id == product_id), None)

    def get_all_products(self):
        return self.products

    def unique_products(self):
        return set(self.products)

    def to_dict(self):
        return {p.id: p.to_dict() for p in self.products}

    def filter_by_price(self, min_price):
        return [p for p in self.products if (lambda x: x >= min_price)(p.price)]


#6
class Logger:
    @staticmethod
    def log_action(user, action, product, filename):
        with open(filename, "a") as f:
            f.write(f"{datetime.now()};{user._id};{action};{product.id}\n")

    @staticmethod
    def read_logs(filename):
        result = []
        try:
            with open(filename) as f:
                for line in f:
                    t, uid, act, pid = line.strip().split(";")
                    result.append({
                        "timestamp": t,
                        "user_id": int(uid),
                        "action": act,
                        "product_id": int(pid)
                    })
        except:
            pass
        return result


#7,8
class Order:
    def __init__(self, id, user, products=None):
        self.id = id
        self.user = user
        self.products = products if products else []

    def add_product(self, product):
        self.products.append(product)

    def remove_product(self, product_id):
        self.products = [p for p in self.products if p.id != product_id]

    def total_price(self):
        return sum(p.price for p in self.products)

    def most_expensive_products(self, n):
        return sorted(self.products, key=lambda x: x.price, reverse=True)[:n]


#9
def price_stream(products):
    for p in products:
        yield p.price


#10
class OrderIterator:
    def __init__(self, orders):
        self.orders = orders
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.orders):
            raise StopIteration
        val = self.orders[self.index]
        self.index += 1
        return val



# NUMPY 11–20

def create_price_array(products):
    return np.array([p.price for p in products], float)

def price_stats(arr):
    return (np.mean(arr), np.median(arr))

def normalize_prices(arr):
    return (arr - arr.min()) / (arr.max() - arr.min()) if arr.max() != arr.min() else np.zeros_like(arr)

def categories_array(products):
    return np.array([p.category for p in products])

def count_unique_categories(arr):
    return len(set(arr))

def above_average_products(arr, products):
    return [p for p in products if p.price > np.mean(arr)]

def apply_discount(arr):
    return arr * 0.9

def orders_to_matrix(orders):
    return np.array([[o.total_price()] for o in orders])

def average_order_value(arr):
    return np.mean(arr)

def expensive_order_indices(arr):
    return list(np.where(arr > 1000)[0])



# PANDAS 21–45

def users_df(users):
    return pd.DataFrame([{
        "id": u._id,
        "name": u._name,
        "email": u._email,
        "registration_date": datetime.now().date()
    } for u in users])

def products_df(products):
    return pd.DataFrame([p.to_dict() for p in products])

def final_report(df):
    res = df.groupby("user_name").agg(
        total_orders=("order_id", "count"),
        total_sum=("total_price", "sum"),
        mean_total=("total_price", "mean"),
        max_order=("total_price", "max"),
        unique_categories=("category", "nunique")
    ).reset_index()
    res["VIP"] = res["total_sum"] > 1000
    return res

#lданные
users = [
    User(1, "john doe", "john@example.com"),
    User(2, "alice", "alice@example.com")
]

products = [
    Product(1, "Laptop", 1200, "Electronics"),
    Product(2, "Mouse", 25, "Electronics"),
    Product(3, "Shirt", 20, "Clothing")
]

orders = [
    Order(1, users[0], [products[0]]),
    Order(2, users[1], [products[1], products[0]])
]


#Выводы
@app.get("/")
def root():
    return {"msg": "FULL PROJECT WORKING 🚀"}

@app.get("/users")
def get_users():
    return [str(u) for u in users]

@app.get("/products")
def get_products():
    return [p.to_dict() for p in products]

@app.get("/inventory/filter")
def inv_filter(min_price: float = 100):
    inv = Inventory()
    for p in products:
        inv.add_product(p)
    return [p.to_dict() for p in inv.filter_by_price(min_price)]

@app.get("/numpy")
def numpy_all():
    arr = create_price_array(products)
    return {
        "prices": arr.tolist(),
        "stats": price_stats(arr),
        "normalized": normalize_prices(arr).tolist(),
        "discount": apply_discount(arr).tolist()
    }

@app.get("/orders")
def orders_api():
    return [{"id": o.id, "total": o.total_price()} for o in orders]

@app.get("/pandas/final")
def pandas_final():
    df = pd.DataFrame([
        {"user_name": "John", "order_id": 1, "total_price": 1200, "category": "Electronics"},
        {"user_name": "John", "order_id": 2, "total_price": 500, "category": "Clothing"},
        {"user_name": "Alice", "order_id": 3, "total_price": 25, "category": "Clothing"}
    ])
    return final_report(df).to_dict(orient="records")