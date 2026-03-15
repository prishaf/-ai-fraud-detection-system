import json
import threading
from fastapi import FastAPI
from kafka import KafkaConsumer

app = FastAPI()

fraud_events = []

def create_consumer():
    return KafkaConsumer(
        "transactions_fraud",
        bootstrap_servers="localhost:9092",
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
        auto_offset_reset="latest",
        group_id="dashboard-v2"
    )

def listen_fraud():
    consumer = create_consumer()
    for message in consumer:
        txn = message.value
        fraud_events.append(txn)

        # Keep only last 100
        if len(fraud_events) > 100:
            fraud_events.pop(0)

        print("📡 Received fraud event")

threading.Thread(target=listen_fraud, daemon=True).start()

@app.get("/events")
def get_events():
    return fraud_events

@app.get("/")
def home():
    return {"message": "Fraud API Running"}
