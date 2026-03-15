#  AI Real-Time Fraud Detection System

A scalable **real-time fraud detection pipeline** designed to process streaming financial transactions and identify suspicious activity using machine learning.

This project demonstrates an **end-to-end data streaming architecture** built with Apache Kafka, where transactions are produced, processed, classified using a trained ML model, and visualized through a live analytics dashboard.

The system simulates real-world **fintech fraud monitoring systems** used in banking and digital payments platforms.

---

#  Project Overview

Financial institutions process millions of transactions every day. Detecting fraudulent activity requires **low-latency streaming systems and intelligent anomaly detection models**.

This project builds a **real-time fraud detection pipeline** that:

• Streams transaction data through Apache Kafka
• Processes events using a consumer service
• Applies a machine learning fraud detection model
• Exposes results through a FastAPI service
• Visualizes fraud analytics through a Streamlit dashboard

---

#  Technology Stack

| Category           | Tools & Frameworks |
| ------------------ | ------------------ |
| Programming        | Python             |
| Streaming Platform | Apache Kafka       |
| Machine Learning   | Scikit-learn       |
| Backend API        | FastAPI            |
| Dashboard          | Streamlit          |
| Containerization   | Docker             |
| Data Processing    | Pandas             |

---

#  Key Features

• Real-time transaction streaming
• Machine learning based fraud detection
• Event-driven streaming architecture
• Fraud analytics dashboard
• Geographical fraud heatmap visualization
• Fraud trend monitoring
• Scalable microservice-based pipeline

---

#  System Architecture

```
Transaction Producer
        ↓
     Apache Kafka
        ↓
 Fraud Detection Consumer
        ↓
   Machine Learning Model
        ↓
      FastAPI Service
        ↓
  Streamlit Dashboard
```

The pipeline follows a **producer-consumer architecture** commonly used in modern real-time data systems.

---

#  Project Structure

```
ai-fraud-detection-system
│
├── producer
│   └── transaction_producer.py
│
├── consumer
│   └── transaction_consumer.py
│
├── api
│   └── api_server.py
│
├── dashboard
│   └── dashboard.py
│
├── model
│   └── fraud_model.pkl
│
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

#  Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ai-fraud-detection-system.git
cd ai-fraud-detection-system
```

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

#  Running the System

### Start Kafka Infrastructure

```bash
docker compose up -d
```

This starts:

• Kafka
• Zookeeper

---

### Run Transaction Producer

```bash
python producer/transaction_producer.py
```

This simulates financial transactions and sends them to Kafka.

---

### Run Fraud Detection Consumer

```bash
python consumer/transaction_consumer.py
```

The consumer:

• Reads transactions from Kafka
• Applies the fraud detection model
• Sends predictions to the API service

---

### Start FastAPI Service

```bash
uvicorn api.api_server:app --reload
```

The API exposes fraud prediction data for the dashboard.

---

### Launch Analytics Dashboard

```bash
streamlit run dashboard/dashboard.py
```

The dashboard provides:

• Live fraud detection results
• Fraud statistics
• Fraud trend visualization
• Geographical fraud heatmap

---

#  Dashboard Analytics

The Streamlit dashboard provides real-time insights including:

• Fraud vs legitimate transaction distribution
• Fraud trends over time
• Geographical fraud activity heatmap
• Live transaction monitoring

---

#  Future Enhancements

• Deep learning fraud detection models
• Real banking transaction datasets
• Cloud deployment (AWS / GCP)
• Kafka Stream processing
• Alerting system for fraud detection
• Database integration for transaction storage

---

#  Support

If you found this project useful, please consider giving it a ⭐ on GitHub.


4. Start API
uvicorn api.api_server:app --reload

5. Run dashboard
streamlit run dashboard/dashboard.py  
