from fastapi import FastAPI
from datetime import datetime
import numpy as np
import pandas as pd
app = FastAPI()
#1
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

class Product:
    def __init__(self,  id: int, name: str, price: float, category: str):
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

#4-5
class Inventory:
    def __init__(self):
        self.products = []

    def add_product(self, product: Product):
        if product.id not in [p.id for p in self.products]:
            self.products.append(product)

    def remove_product(self, product_id: int):
        self.products = [p for p in self.products if p.id != product_id]

    def get_product(self, product_id: int):
        return next((p for p in self.products if p.id == product_id), None)

    def get_all_products(self):
        return self.products

    def unique_products(self):
        return set(self.products)

    def to_dict(self):
        return {p.id: p.to_dict() for p in self.products}

    def filter_by_price(self, min_price: float):
        return [p for p in self.products if (lambda x: x >= min_price)(p.price)]

#6
class Logger:
    @staticmethod
    def log_action(user: User, action: str, product: Product, filename: str):
        with open(filename, "a") as f:
            line = f"{datetime.now()};{user._id};{action};{product.id}\n"
            f.write(line)

    @staticmethod
    def read_logs(filename: str):
        result = []
        with open(filename, "r") as f:
            for line in f:
                t, uid, act, pid = line.strip().split(";")
                result.append({
                    "timestamp": t,
                    "user_id": int(uid),
                    "action": act,
                    "product_id": int(pid)
                })
        return result

#7-8
class Order:
    def __init__(self, id: int, user: User, products=None):
        self.id = id
        self.user = user
        self.products = products if products else []

    def add_product(self, product: Product):
        self.products.append(product)

    def remove_product(self, product_id: int):
        self.products = [p for p in self.products if p.id != product_id]

    def total_price(self):
        return sum(p.price for p in self.products)

    def most_expensive_products(self, n: int):
        return sorted(self.products, key=lambda x: x.price, reverse=True)[:n]

    def __str__(self):
        return f"Order(id={self.id}, total={self.total_price()})"


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


#NUMPY
##=11
def create_price_array(products):
    return np.array([p.price for p in products], dtype=float)

#12
def price_stats(price_array):
    mean_price = np.mean(price_array)
    median_price = np.median(price_array)
    return(mean_price, median_price)

#13
def normalize_prices(price_array):
    min_val = np.min(price_array)
    max_val = np.max(price_array)

    if max_val == min_val:
        return np.zeros_like(price_array)

    return (price_array - min_val) / (max_val - min_val)

#14
def categories_array(products):
    return np.array([p.category for p in products])

#15
def count_unique_categories(category_array):
    return len(set(category_array))

#16
def above_average_products(price_array, products):
    mean_price = np.mean(price_array)
    return [p for p in products if p.price > mean_price]

#17
def apply_discount(price_array, discount=0.10):
    return price_array * (1 - discount)

#18
def orders_to_matrix(orders):
    return np.array([[order.total_price()] for order in orders])

#19
def average_order_value(order_totals):
    return np.mean(order_totals)

#20
def expensive_order_indices(order_totals, threshold=1000):
    return list(np.where(order_totals > threshold)[0])

#PANDAS
#21
def users_to_dataframe(users):
    data = []
    today = datetime.now().date()
    for i in users:
        data.append({
            "id": i._id,
            "name": i._name,
            "email": i._email,
            "registration_date": today
        })
    return pd.DataFrame(data)

#22
def products_to_dataframe(products):
    data = [p.to_dict() for p in products]
    return pd.DataFrame(data)[["id", "name", "category", "price"]]

#23
def merge_users_orders(users_df, orders_df):
    merged = pd.merge(
        orders_df,
        users_df,
        left_on = "user_id",
        right_on="id"
    )
    return merged[["order_id", "name", "total"]].rename(columns={"name": "user_name"})

#24
def filter_orders(df, min_total):
    return df[df["total"] > min_total]

#25
def total_by_user(df):
    result = df.groupby("user_name")["total"].sum().reset_index()
    return result.rename(columns={"total": "total_sum"})

#26
def mean_by_user(df):
    result = df.groupby("user_name")["total"].mean().reset_index()
    return result.rename(columns={"total": "mean_total"})

#27
def count_orders_by_user(df):
    result = df.groupby("user_name")["total"].count().reset_index()
    return result.rename(columns={"total": "orders_count"})

#28
def mean_price_by_category(products_df):
    result = products_df.groupby("category")["price"].mean().reset_index()
    return result.rename(columns={"price": "mean_price"})

#29
def add_discount_column(products_df, discount=0.10):
    products_df["discounted_price"] = products_df["price"] * (1 - discount)
    return products_df

#30
def sort_products_by_price(products_df):
    return products_df.sort_values(by="price", ascending=False)

#31
def add_quantity(df):
    df["quantity"] = 1
    return df


#32
def add_total_price(df):
    df["total_price"] = df["price"] * df["quantity"]
    return df


#33
def filter_by_category(df, category="Electronics"):
    return df[df["category"] == category]


#34
def count_products_by_category(df):
    result = df.groupby("category").size().reset_index(name="count")
    return result


#35
def mean_price_category(df):
    result = df.groupby("category")["price"].mean().reset_index()
    return result.rename(columns={"price": "mean_price"})


#36
def sort_orders(df):
    return df.sort_values(by="total_price", ascending=False)


#37
def top_n_orders(df, n=3):
    return df.sort_values(by="total_price", ascending=False).head(n)


#38
def merge_users_orders_v2(users_df, orders_df):
    merged = pd.merge(orders_df, users_df, on="user_id")
    return merged[["order_id", "user_name", "total_price"]]


#39
def mean_order_per_user(df):
    result = df.groupby("user_name")["total_price"].mean().reset_index()
    return result.rename(columns={"total_price": "mean_total"})


#40
def count_orders(df):
    result = df.groupby("user_name")["order_id"].count().reset_index()
    return result.rename(columns={"order_id": "orders_count"})


#41
def max_order_per_user(df):
    result = df.groupby("user_name")["total_price"].max().reset_index()
    return result.rename(columns={"total_price": "max_order"})


#42
def unique_categories_per_user(df):
    result = df.groupby("user_name")["category"].nunique().reset_index()
    return result.rename(columns={"category": "unique_categories"})


#43
def add_vip(df):
    df["VIP"] = df["total_sum"] > 1000
    return df


#44
def sort_users(df):
    return df.sort_values(by=["total_sum", "mean_total"], ascending=[False, True])


#45
def final_report(df):
    total_orders = df.groupby("user_name")["order_id"].count()
    total_sum = df.groupby("user_name")["total_price"].sum()
    mean_total = df.groupby("user_name")["total_price"].mean()
    max_order = df.groupby("user_name")["total_price"].max()
    unique_categories = df.groupby("user_name")["category"].nunique()

    result = pd.DataFrame({
        "total_orders": total_orders,
        "total_sum": total_sum,
        "mean_total": mean_total,
        "max_order": max_order,
        "unique_categories": unique_categories
    }).reset_index()

    result["VIP"] = result["total_sum"] > 1000

    return result



if __name__ == "__main__":
    df = pd.DataFrame([
        {"user_name": "John", "order_id": 101, "total_price": 1200, "category": "Electronics", "price": 1200},
        {"user_name": "John", "order_id": 103, "total_price": 500, "category": "Clothing", "price": 500},
        {"user_name": "Alice", "order_id": 102, "total_price": 25, "category": "Clothing", "price": 25}
    ])

    df = add_quantity(df)
    df = add_total_price(df)

    print(filter_by_category(df))

    print(count_products_by_category(df))
    print(mean_price_category(df))

    print(sort_orders(df))
    print(top_n_orders(df))

    print(mean_order_per_user(df))
    print(count_orders(df))
    print(max_order_per_user(df))
    print(unique_categories_per_user(df))

    report = final_report(df)
    print(report)

    print(add_vip(report))
    print(sort_users(report))

