import json
import time
import random
from datetime import datetime, timezone
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

TOPIC = "transactions_raw"

users = [f"user_{i}" for i in range(1, 21)]
merchants = ["Amazon", "Flipkart", "Swiggy", "Zomato", "Myntra"]
locations = ["Mumbai", "Delhi", "Bangalore", "Pune", "Hyderabad"]
devices = ["android", "ios", "web"]

def generate_transaction():
    return {
        "transaction_id": f"txn_{random.randint(100000,999999)}",
        "user_id": random.choice(users),
        "amount": round(random.uniform(100, 50000), 2),
        "merchant": random.choice(merchants),
        "location": random.choice(locations),
        "device": random.choice(devices),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

while True:
    try:
        producer = KafkaProducer(
            bootstrap_servers="localhost:9092",
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )
        print("✅ Producer connected to Kafka")
        break
    except NoBrokersAvailable:
        print("⏳ Waiting for Kafka...")
        time.sleep(5)

print("🚀 Sending transactions...")

while True:
    txn = generate_transaction()
    producer.send(TOPIC, txn)
    producer.flush()
    print("Sent:", txn["transaction_id"])
    time.sleep(1)
