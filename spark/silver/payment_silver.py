from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    to_timestamp,
    trim,
    upper
)

spark = (
    SparkSession.builder
    .appName("PaymentSilver")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

# Read Bronze data
bronze_df = spark.read.parquet("spark/bronze/payments")

# Clean and transform
silver_df = (
    bronze_df
    .withColumn("payment_method", upper(trim(col("payment_method"))))
    .withColumn("payment_status", upper(trim(col("payment_status"))))
    .withColumn(
        "payment_timestamp",
        to_timestamp(col("payment_timestamp"))
    )
    .filter(col("payment_id").isNotNull())
    .filter(col("order_id").isNotNull())
    .filter(col("payment_amount").isNotNull())
)

# Write Silver data
(
    silver_df.write
    .mode("overwrite")
    .parquet("spark/silver/payments")
)

print("Silver transformation completed.")
print(f"Silver records: {silver_df.count()}")

spark.stop()
