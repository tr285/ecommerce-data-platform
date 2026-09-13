
import os
import random
from datetime import datetime, timedelta

import pandas as pd
from faker import Faker

fake = Faker()

OUTPUT_DIR = "../../data/raw"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------------------------
# Customers
# -------------------------

customers = []

for i in range(1, 1001):
    customers.append({
        "customer_id": i,
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.unique.email(),
        "city": fake.city(),
        "country": fake.country(),
        "created_at": fake.date_time_between(
            start_date="-2y",
            end_date="now"
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
        "stock_quantity": random.randint(0, 500),
        "created_at": fake.date_time_between(
            start_date="-2y",
            end_date="now"
        )
    })

products_df = pd.DataFrame(products)

# -------------------------
# Orders + Order Items
# -------------------------

orders = []
order_items = []

start_date = datetime.now() - timedelta(days=365)

for order_id in range(1, 10001):

    customer_id = random.randint(1, 1000)
    product = random.choice(products)

    product_id = product["product_id"]
    quantity = random.randint(1, 5)
    unit_price = product["price"]

    total_amount = round(
        unit_price * quantity,
        2
    )

    order_status = random.choice([
        "COMPLETED",
        "COMPLETED",
        "COMPLETED",
        "CANCELLED",
        "PENDING"
    ])

    order_date = start_date + timedelta(
        minutes=random.randint(0, 525600)
    )

    # Orders
    orders.append({
        "order_id": order_id,
        "customer_id": customer_id,
        "order_date": order_date,
        "total_amount": total_amount,
        "status": order_status
    })

    # Order items
    order_items.append({
        "order_item_id": order_id,
        "order_id": order_id,
        "product_id": product_id,
        "quantity": quantity,
        "unit_price": unit_price
    })

orders_df = pd.DataFrame(orders)
order_items_df = pd.DataFrame(order_items)

# -------------------------
# Save CSV files
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

order_items_df.to_csv(
    f"{OUTPUT_DIR}/order_items.csv",
    index=False
)

print("Data generation completed.")
print(f"Customers: {len(customers_df)}")
print(f"Products: {len(products_df)}")
print(f"Orders: {len(orders_df)}")
print(f"Order Items: {len(order_items_df)}")
