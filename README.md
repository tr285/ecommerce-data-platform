# E-Commerce Data Engineering Platform

An end-to-end data engineering project that processes e-commerce payment data using Kafka, Apache Spark, and Databricks.

## Architecture

CSV / PostgreSQL
       ↓
     Kafka
       ↓
 Databricks
       ↓
Bronze Delta
       ↓
Silver Delta
       ↓
Gold Delta
       ↓
Databricks SQL Dashboard

## Technologies

- Python
- PostgreSQL
- Apache Kafka
- Apache Spark / PySpark
- Databricks
- Delta Lake
- Databricks SQL
- Git & GitHub

## Data Pipeline

### Bronze
Raw payment events are ingested from Kafka and stored in:

`main.ecommerce.bronze_payments`

Records: 10,000

### Silver
Payment data is cleaned, standardized, validated and deduplicated.

Table:

`main.ecommerce.silver_payments`

Records: 10,000

### Gold

Three analytical tables are created:

- `main.ecommerce.gold_payment_summary`
- `main.ecommerce.gold_payment_method`
- `main.ecommerce.gold_daily_payments`

## Dashboard

The Databricks SQL dashboard provides:

- Total payment KPIs
- Payment revenue analysis
- Payment method analysis
- Payment success rates
- Daily revenue trends
- Daily success-rate trends
- Payment status distribution

## Key Results

- Total Payments: 10,000
- Total Payment Amount: $31.55M
- Successful Payments: 6,003
- Failed Payments: 2,022
- Pending Payments: 1,975
- Overall Success Rate: 60.03%
- Highest Payment Method Success Rate: WALLET — 61.44%

## Project Structure

```text
ecommerce-data-platform/
├── README.md
├── data/
│   ├── raw/
│   └── processed/
├── src/
│   ├── ingestion/
│   ├── transformation/
│   ├── streaming/
│   └── quality/
├── kafka/
└── spark/
    ├── bronze/
    ├── silver/
    └── gold/
