import json
import pandas as pd
from kafka import KafkaProducer

KAFKA_SERVER = "localhost:9094"
TOPIC = "payments"

DATA_FILE = "../../data/raw/payments.csv"

payments_df = pd.read_csv(DATA_FILE)

producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda value: json.dumps(value).encode("utf-8")
)

for _, row in payments_df.iterrows():

    payment = {
        "payment_id": int(row["payment_id"]),
        "order_id": int(row["order_id"]),
        "payment_method": row["payment_method"],
        "payment_status": row["payment_status"],
        "payment_amount": float(row["payment_amount"]),
        "payment_timestamp": row["payment_timestamp"]
    }

    producer.send(
        TOPIC,
        value=payment
    )

producer.flush()
producer.close()

print(f"Successfully sent {len(payments_df)} payments to Kafka.")