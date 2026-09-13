import os
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from databricks import sql


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)

DATABRICKS_SERVER_HOSTNAME = os.getenv("DATABRICKS_SERVER_HOSTNAME")
DATABRICKS_HTTP_PATH = os.getenv("DATABRICKS_HTTP_PATH")
DATABRICKS_TOKEN = os.getenv("DATABRICKS_TOKEN")

if not all(
    [
        DATABRICKS_SERVER_HOSTNAME,
        DATABRICKS_HTTP_PATH,
        DATABRICKS_TOKEN,
    ]
):
    raise RuntimeError(
        "Missing Databricks configuration. "
        "Check backend/.env"
    )


# ---------------------------------------------------------
# FastAPI
# ---------------------------------------------------------

app = FastAPI(
    title="E-Commerce Data Platform API",
    description="REST API powered by Databricks Gold Delta tables",
    version="1.0.0",
)


# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# Databricks connection
# ---------------------------------------------------------

def get_connection():
    return sql.connect(
        server_hostname=DATABRICKS_SERVER_HOSTNAME,
        http_path=DATABRICKS_HTTP_PATH,
        access_token=DATABRICKS_TOKEN,
    )


# ---------------------------------------------------------
# JSON conversion
# ---------------------------------------------------------

def make_json_safe(value):
    if isinstance(value, Decimal):
        return float(value)

    if isinstance(value, (datetime, date)):
        return value.isoformat()

    return value


# ---------------------------------------------------------
# Execute SQL
# ---------------------------------------------------------

def execute_query(query: str):
    connection = None

    try:
        connection = get_connection()

        with connection.cursor() as cursor:
            cursor.execute(query)

            if cursor.description is None:
                return []

            columns = [column[0] for column in cursor.description]
            rows = cursor.fetchall()

            result = []

            for row in rows:
                record = {}

                for column, value in zip(columns, row):
                    record[column] = make_json_safe(value)

                result.append(record)

            return result

    except Exception as error:
        print(f"Databricks error: {error}")

        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve data from Databricks.",
        )

    finally:
        if connection:
            connection.close()


# ---------------------------------------------------------
# Root
# ---------------------------------------------------------

@app.get("/")
def root():
    return {
        "application": "E-Commerce Data Platform API",
        "status": "running",
        "data_source": "Databricks Gold Delta Tables",
    }


# ---------------------------------------------------------
# Health
# ---------------------------------------------------------

@app.get("/health")
def health():
    try:
        result = execute_query("SELECT 1")

        return {
            "status": "healthy",
            "databricks": "connected",
            "test": result,
        }

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Databricks connection unavailable.",
        )


# ---------------------------------------------------------
# Payment Summary
# ---------------------------------------------------------

@app.get("/api/summary")
def get_summary():
    return execute_query(
        """
        SELECT
            total_payments,
            total_payment_amount,
            successful_payments,
            failed_payments,
            pending_payments,
            successful_payment_amount,
            failed_payment_amount,
            success_rate_percentage
        FROM main.ecommerce.gold_payment_summary
        """
    )


# ---------------------------------------------------------
# Payment Methods
# ---------------------------------------------------------

@app.get("/api/payment-methods")
def get_payment_methods():
    return execute_query(
        """
        SELECT
            payment_method,
            total_payments,
            total_payment_amount,
            successful_payments,
            success_rate_percentage
        FROM main.ecommerce.gold_payment_method
        ORDER BY total_payment_amount DESC
        """
    )


# ---------------------------------------------------------
# Daily Payments
# ---------------------------------------------------------

@app.get("/api/daily-payments")
def get_daily_payments():
    return execute_query(
        """
        SELECT
            payment_date,
            total_payments,
            total_payment_amount,
            successful_payments,
            success_rate_percentage
        FROM main.ecommerce.gold_daily_payments
        ORDER BY payment_date
        """
    )