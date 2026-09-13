
import pandas as pd
from sqlalchemy import create_engine

# PostgreSQL connection
DATABASE_URL = "postgresql+psycopg2://tukaramgore@localhost:5432/ecommerce_db"

DATA_FILE = "../../data/raw/payments.csv"

# Create database connection
engine = create_engine(DATABASE_URL)

# Read payment CSV
payments_df = pd.read_csv(DATA_FILE)

# Convert timestamp
payments_df["payment_timestamp"] = pd.to_datetime(
    payments_df["payment_timestamp"]
)

# Load into PostgreSQL
payments_df.to_sql(
    "payments",
    engine,
    if_exists="append",
    index=False
)

print("Payment data loaded successfully.")
print(f"Payments loaded: {len(payments_df)}")

