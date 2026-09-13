from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import (
    StructType,
    StructField,
    IntegerType,
    StringType,
    DoubleType
)

spark = (
    SparkSession.builder
    .appName("PaymentBronzeStreaming")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

# Payment schema
payment_schema = StructType([
    StructField("payment_id", IntegerType(), True),
    StructField("order_id", IntegerType(), True),
    StructField("payment_method", StringType(), True),
    StructField("payment_status", StringType(), True),
    StructField("payment_amount", DoubleType(), True),
    StructField("payment_timestamp", StringType(), True)
])

# Read from Kafka
kafka_df = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9094")
    .option("subscribe", "payments")
    .option("startingOffsets", "earliest")
    .load()
)

# Convert Kafka value from binary to string
json_df = kafka_df.select(
    from_json(
        col("value").cast("string"),
        payment_schema
    ).alias("payment")
)

payments_df = json_df.select("payment.*")

# Write Bronze data
query = (
    payments_df.writeStream
    .format("parquet")
    .outputMode("append")
    .option("path", "spark/bronze/payments")
    .option("checkpointLocation", "spark/bronze/checkpoints/payments")
    .start()
)

query.awaitTermination()
