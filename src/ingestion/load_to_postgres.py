
import pandas as pd
from sqlalchemy import create_engine

# PostgreSQL connection
DATABASE_URL = "postgresql+psycopg2://tukaramgore@localhost:5432/ecommerce_db"

engine = create_engine(DATABASE_URL)

DATA_DIR = "../../data/raw"


def load_table(file_name, table_name):
    file_path = f"{DATA_DIR}/{file_name}"

    df = pd.read_csv(file_path)

    df.to_sql(
        table_name,
        engine,
        if_exists="append",
        index=False
    )

    print(f"{table_name}: {len(df)} rows loaded")


# Load tables in foreign-key order
load_table("customers.csv", "customers")
load_table("products.csv", "products")
load_table("orders.csv", "orders")
load_table("order_items.csv", "order_items")

print("================================")
print("PostgreSQL loading completed!")
print("================================")

