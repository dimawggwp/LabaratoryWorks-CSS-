from fastapi import FastAPI
from datetime import datetime
import numpy as np
import pandas as pd
import os
app = FastAPI()
#Классы

class User:
    def __init__(self, id: int, name: str, email: str):
        self._id = id
        self._name = name.strip().title()
        self._email = email.strip().lower()
        if "@" not in self._email:
            raise ValueError("Invalid email")

    def __str__(self):
        return f"User(id={self._id}, name='{self._name}', email='{self._email}')"

    @classmethod
    def from_string(cls, data: str):
        parts = data.split(",")
        return cls(int(parts[0].strip()), parts[1].strip(), parts[2].strip())


class Product:
    def __init__(self, id, name, price, category):
        self.id = id
        self.name = name
        self.price = price
        self.category = category

    def __str__(self):
        return f"Product({self.name}, {self.price})"

    def __eq__(self, other):
        return isinstance(other, Product) and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "price": float(self.price), "category": self.category}


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
        return list(set(self.products))

    def to_dict(self):
        return {p.id: p.to_dict() for p in self.products}

    def filter_by_price(self, min_price):
        return [p for p in self.products if p.price >= min_price]


class Logger:
    @staticmethod
    def log_action(user, action, product, filename):
        with open(filename, "a") as f:
            f.write(f"{datetime.now()};{user._id};{action};{product.id}\n")

    @staticmethod
    def read_logs(filename):
        if not os.path.exists(filename):
            return []
        with open(filename, "r") as f:
            result = []
            for line in f:
                t, uid, act, pid = line.strip().split(";")
                result.append({
                    "timestamp": t,
                    "user_id": int(uid),
                    "action": act,
                    "product_id": int(pid)
                })
            return result


class Order:
    def __init__(self, id, user, products=None):
        self.id = id
        self.user = user
        self.products = products or []

    def add_product(self, product):
        self.products.append(product)

    def remove_product(self, product_id):
        self.products = [p for p in self.products if p.id != product_id]

    def total_price(self):
        return float(sum(p.price for p in self.products))

    def most_expensive_products(self, n):
        return sorted(self.products, key=lambda x: x.price, reverse=True)[:n]

####

def price_stream(products):
    for p in products:
        yield float(p.price)


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



def create_price_array(products):
    return np.array([p.price for p in products], dtype=float)

def price_stats(arr):
    return float(np.mean(arr)), float(np.median(arr))

def normalize_prices(arr):
    if arr.max() == arr.min():
        return np.zeros_like(arr).tolist()
    return ((arr - arr.min()) / (arr.max() - arr.min())).tolist()

def categories_array(products):
    return np.array([p.category for p in products])

def count_unique_categories(arr):
    return int(len(set(arr)))

def above_average_products(arr, products):
    return [p for p in products if p.price > float(np.mean(arr))]

def apply_discount(arr):
    return (arr * 0.9).tolist()

def orders_to_matrix(orders):
    return np.array([[o.total_price()] for o in orders])

def average_order_value(matrix):
    return float(np.mean(matrix))

def expensive_order_indices(matrix):
    return list(map(int, np.where(matrix > 1000)[0]))


#Классы

def users_to_dataframe(users):
    return pd.DataFrame([{
        "id": u._id,
        "name": u._name,
        "email": u._email,
        "registration_date": str(datetime.now().date())
    } for u in users])

def products_to_dataframe(products):
    return pd.DataFrame([p.to_dict() for p in products])

def merge_users_orders(users_df, orders_df):
    merged = pd.merge(
        orders_df,
        users_df,
        left_on="user_id",
        right_on="id",
        suffixes=("_order", "_user")
    )

    return merged[["order_id", "name", "total"]].rename(
        columns={"name": "user_name"}
    )

def filter_orders(df, min_total):
    return df[df["total"] > min_total]

def total_by_user(df):
    return df.groupby("user_name")["total"].sum().reset_index(name="total_sum")

def mean_by_user(df):
    return df.groupby("user_name")["total"].mean().reset_index(name="mean_total")

def count_orders_by_user(df):
    return df.groupby("user_name")["total"].count().reset_index(name="orders_count")

def mean_price_by_category(df):
    return df.groupby("category")["price"].mean().reset_index(name="mean_price")

def add_discount_column(df):
    df["discounted_price"] = df["price"] * 0.9
    return df

def sort_products_by_price(df):
    return df.sort_values(by="price", ascending=False)

def add_quantity(df):
    df["quantity"] = 1
    return df

def add_total_price(df):
    df["total_price"] = df["price"] * df["quantity"]
    return df

def filter_by_category(df, category="Electronics"):
    return df[df["category"] == category]

def count_products_by_category(df):
    return df.groupby("category").size().reset_index(name="count")

def mean_price_category(df):
    return df.groupby("category")["price"].mean().reset_index(name="mean_price")

def sort_orders(df):
    return df.sort_values(by="total_price", ascending=False)

def top_n_orders(df, n=3):
    return df.sort_values(by="total_price", ascending=False).head(n)

def merge_users_orders_v2(users_df, orders_df):
    return pd.merge(orders_df, users_df, on="user_id")

def mean_order_per_user(df):
    return df.groupby("user_name")["total_price"].mean().reset_index(name="mean_total")
#40
def count_orders(df):
    return df.groupby("user_name")["order_id"].count().reset_index(name="orders_count")
#41
def max_order_per_user(df):
    return df.groupby("user_name")["total_price"].max().reset_index(name="max_order")
#42
def unique_categories_per_user(df):
    return df.groupby("user_name")["category"].nunique().reset_index(name="unique_categories")
#43
def add_vip(df):
    df["VIP"] = df["total_sum"] > 1000
    return df
#44
def sort_users(df):
    return df.sort_values(by=["total_sum", "mean_total"], ascending=[False, True])



#Вывод

@app.get("/task1")
def task1():
    return str(User(1, " john ", "TEST@MAIL.COM"))

@app.get("/task2")
def task2():
    return str(User.from_string("2, alice, alice@mail.com"))

@app.get("/task3")
def task3():
    return Product(1, "A", 10, "Cat") == Product(1, "B", 20, "Cat")

@app.get("/task4")
def task4():
    _, products, _ = sample_data()
    inv = Inventory()
    for p in products:
        inv.add_product(p)
    return [str(p) for p in inv.get_all_products()]

@app.get("/task6")
def task6():
    user, products, _ = sample_data()
    Logger.log_action(user, "buy", products[0], "log.txt")
    return Logger.read_logs("log.txt")

@app.get("/task7")
def task7():
    _, _, order = sample_data()
    return order.total_price()

@app.get("/task8")
def task8():
    _, _, order = sample_data()
    return [p.name for p in order.most_expensive_products(2)]

@app.get("/task9")
def task9():
    _, products, _ = sample_data()
    return list(price_stream(products))

@app.get("/task10")
def task10():
    _, _, order = sample_data()
    return [str(o) for o in OrderIterator([order])]

@app.get("/task11")
def task11():
    _, products, _ = sample_data()
    return create_price_array(products).tolist()

@app.get("/task12")
def task12():
    _, products, _ = sample_data()
    mean, median = price_stats(create_price_array(products))
    return {"mean": mean, "median": median}

@app.get("/task13")
def task13():
    _, products, _ = sample_data()
    return normalize_prices(create_price_array(products))

@app.get("/task14")
def task14():
    _, products, _ = sample_data()
    return categories_array(products).tolist()

@app.get("/task15")
def task15():
    _, products, _ = sample_data()
    return count_unique_categories(categories_array(products))

@app.get("/task16")
def task16():
    _, products, _ = sample_data()
    return [p.name for p in above_average_products(create_price_array(products), products)]

@app.get("/task17")
def task17():
    _, products, _ = sample_data()
    return apply_discount(create_price_array(products))

@app.get("/task18")
def task18():
    _, _, order = sample_data()
    return orders_to_matrix([order]).tolist()

@app.get("/task19")
def task19():
    _, _, order = sample_data()
    return average_order_value(orders_to_matrix([order]))

@app.get("/task20")
def task20():
    _, _, order = sample_data()
    return expensive_order_indices(orders_to_matrix([order]))

@app.get("/task21")
def task21():
    user, _, _ = sample_data()
    return users_to_dataframe([user]).to_dict(orient="records")

@app.get("/task22")
def task22():
    _, products, _ = sample_data()
    return products_to_dataframe(products).to_dict(orient="records")

@app.get("/task23")
def task23():
    user, _, order = sample_data()
    users_df = users_to_dataframe([user])
    orders_df = pd.DataFrame([{"order_id": order.id, "user_id": user._id, "total": order.total_price()}])
    return merge_users_orders(users_df, orders_df).to_dict(orient="records")

@app.get("/task24")
def task24():
    df = pd.DataFrame([{"total": 100}, {"total": 200}])
    return filter_orders(df, 150).to_dict(orient="records")

@app.get("/task25")
def task25():
    df = pd.DataFrame([{"user_name": "A", "total": 100}])
    return total_by_user(df).to_dict(orient="records")

@app.get("/task26")
def task26():
    df = pd.DataFrame([{"user_name": "A", "total": 100}])
    return mean_by_user(df).to_dict(orient="records")

@app.get("/task27")
def task27():
    df = pd.DataFrame([{"user_name": "A", "total": 100}])
    return count_orders_by_user(df).to_dict(orient="records")

@app.get("/task28")
def task28():
    _, products, _ = sample_data()
    return mean_price_by_category(products_to_dataframe(products)).to_dict(orient="records")

@app.get("/task29")
def task29():
    _, products, _ = sample_data()
    return add_discount_column(products_to_dataframe(products)).to_dict(orient="records")

@app.get("/task30")
def task30():
    _, products, _ = sample_data()
    return sort_products_by_price(products_to_dataframe(products)).to_dict(orient="records")

@app.get("/task31")
def task31():
    return add_quantity(pd.DataFrame([{"price": 10}])).to_dict(orient="records")

@app.get("/task32")
def task32():
    return add_total_price(pd.DataFrame([{"price": 10, "quantity": 2}])).to_dict(orient="records")

@app.get("/task33")
def task33():
    return filter_by_category(pd.DataFrame([{"category": "Electronics"}])).to_dict(orient="records")

@app.get("/task34")
def task34():
    return count_products_by_category(pd.DataFrame([{"category": "A"}, {"category": "A"}])).to_dict(orient="records")

@app.get("/task35")
def task35():
    return mean_price_category(pd.DataFrame([{"category": "A", "price": 10}])).to_dict(orient="records")

@app.get("/task36")
def task36():
    return sort_orders(pd.DataFrame([{"total_price": 10}])).to_dict(orient="records")

@app.get("/task37")
def task37():
    return top_n_orders(pd.DataFrame([{"total_price": 10}])).to_dict(orient="records")

@app.get("/task38")
def task38():
    df1 = pd.DataFrame([{"user_id": 1, "user_name": "A"}])
    df2 = pd.DataFrame([{"user_id": 1, "order_id": 1, "total_price": 100}])
    return merge_users_orders_v2(df1, df2).to_dict(orient="records")

@app.get("/task39")
def task39():
    return mean_order_per_user(pd.DataFrame([{"user_name": "A", "total_price": 100}])).to_dict(orient="records")

@app.get("/task40")
def task40():
    return count_orders(pd.DataFrame([{"user_name": "A", "order_id": 1}])).to_dict(orient="records")

@app.get("/task41")
def task41():
    return max_order_per_user(pd.DataFrame([{"user_name": "A", "total_price": 100}])).to_dict(orient="records")

@app.get("/task42")
def task42():
    return unique_categories_per_user(pd.DataFrame([{"user_name": "A", "category": "X"}])).to_dict(orient="records")

@app.get("/task43")
def task43():
    return add_vip(pd.DataFrame([{"user_name": "A", "total_sum": 1500}])).to_dict(orient="records")

@app.get("/task44")
def task44():
    return sort_users(pd.DataFrame([{"total_sum": 100, "mean_total": 50}])).to_dict(orient="records")

@app.get("/task45")
def task45():
    df = pd.DataFrame([{"user_name": "A", "order_id": 1, "total_price": 100, "category": "X"}])
    return final_report(df).to_dict(orient="records")