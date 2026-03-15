import json
import time
from kafka import KafkaConsumer, KafkaProducer
from sklearn.ensemble import IsolationForest
import numpy as np

print("🚀 AI Fraud Detection Service Starting...")

consumer = KafkaConsumer(
    "transactions_raw",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    auto_offset_reset="latest",
    group_id="ai-fraud-v1"
)

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda x: json.dumps(x).encode("utf-8")
)

model = IsolationForest(contamination=0.1, random_state=42)

buffer = []

for message in consumer:
    txn = message.value
    buffer.append(txn["amount"])

    if len(buffer) > 50:
        buffer.pop(0)

    if len(buffer) >= 20:
        X = np.array(buffer).reshape(-1, 1)
        model.fit(X)

        score = abs(model.decision_function([[txn["amount"]]])[0])
        prediction = model.predict([[txn["amount"]]])[0]

        risk = "HIGH" if prediction == -1 else "LOW"

        txn["fraud_score"] = round(score * 10, 2)
        txn["risk"] = risk

        if risk == "HIGH":
            producer.send("transactions_fraud", txn)
        else:
            producer.send("transactions_clean", txn)

        producer.flush()

        print(f"[AI] {txn['transaction_id']} | score={txn['fraud_score']} | risk={risk}")
