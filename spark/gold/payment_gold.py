from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    count,
    sum,
    round
)

spark = (
    SparkSession.builder
    .appName("PaymentGold")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

# Read Silver data
silver_df = spark.read.parquet("spark/silver/payments")

# Create business-level payment summary
gold_df = (
    silver_df
    .groupBy("payment_method", "payment_status")
    .agg(
        count("payment_id").alias("total_payments"),
        round(sum("payment_amount"), 2).alias("total_payment_amount")
    )
    .orderBy("payment_method", "payment_status")
)

# Write Gold data
(
    gold_df.write
    .mode("overwrite")
    .parquet("spark/gold/payment_summary")
)

print("Gold transformation completed.")

gold_df.show(truncate=False)

spark.stop()
