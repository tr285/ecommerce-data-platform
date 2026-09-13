import os
import random
import pandas as pd
from datetime import datetime, timedelta

OUTPUT_DIR = "../../data/raw"
os.makedirs(OUTPUT_DIR, exist_ok=True)

orders = pd.read_csv("data/raw/orders.csv")

payment_methods = [
    "CREDIT_CARD",
    "DEBIT_CARD",
    "UPI",
    "NET_BANKING",
    "WALLET"
]

payment_statuses = [
    "SUCCESS",
    "SUCCESS",
    "SUCCESS",
    "FAILED",
    "PENDING"
]

payments = []

for payment_id, (_, order) in enumerate(orders.iterrows(), start=1):

    payments.append({
        "payment_id": payment_id,
        "order_id": order["order_id"],
        "payment_method": random.choice(payment_methods),
        "payment_status": random.choice(payment_statuses),
        "payment_amount": order["order_amount"],
        "payment_timestamp": (
            pd.to_datetime(order["order_timestamp"])
            + timedelta(minutes=random.randint(1, 30))
        )
    })

payments_df = pd.DataFrame(payments)

payments_df.to_csv(
    f"{OUTPUT_DIR}/payments.csv",
    index=False
)

print("Payment data generated.")
print("Payments:", len(payments_df))