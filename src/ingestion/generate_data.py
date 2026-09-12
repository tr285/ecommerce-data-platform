import os
import random
from datetime import datetime, timedelta

import pandas as pd
from faker import Faker

fake = Faker()

OUTPUT_DIR = "data/raw"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------------------------
# Customers
# -------------------------

customers = []

for i in range(1, 1001):
    customers.append({
        "customer_id": i,
        "customer_name": fake.name(),
        "email": fake.email(),
        "city": fake.city(),
        "state": fake.state(),
        "signup_date": fake.date_between(
            start_date="-2y",
            end_date="today"
        )
    })

customers_df = pd.DataFrame(customers)

# -------------------------
# Products
# -------------------------

categories = [
    "Electronics",
    "Clothing",
    "Home",
    "Books",
    "Sports"
]

products = []

for i in range(1, 201):
    products.append({
        "product_id": i,
        "product_name": fake.catch_phrase(),
        "category": random.choice(categories),
        "price": round(random.uniform(10, 2000), 2),
        "stock": random.randint(0, 500)
    })

products_df = pd.DataFrame(products)

# -------------------------
# Orders
# -------------------------

orders = []

start_date = datetime.now() - timedelta(days=365)

for i in range(1, 10001):

    product = random.choice(products)
    quantity = random.randint(1, 5)

    orders.append({
        "order_id": i,
        "customer_id": random.randint(1, 1000),
        "product_id": product["product_id"],
        "quantity": quantity,
        "order_amount": round(product["price"] * quantity, 2),
        "order_status": random.choice([
            "COMPLETED",
            "COMPLETED",
            "COMPLETED",
            "CANCELLED",
            "PENDING"
        ]),
        "order_timestamp": start_date + timedelta(
            minutes=random.randint(0, 525600)
        )
    })

orders_df = pd.DataFrame(orders)

# -------------------------
# Save files
# -------------------------

customers_df.to_csv(
    f"{OUTPUT_DIR}/customers.csv",
    index=False
)

products_df.to_csv(
    f"{OUTPUT_DIR}/products.csv",
    index=False
)

orders_df.to_csv(
    f"{OUTPUT_DIR}/orders.csv",
    index=False
)

print("Data generation completed.")
print(f"Customers: {len(customers_df)}")
print(f"Products: {len(products_df)}")
print(f"Orders: {len(orders_df)}")