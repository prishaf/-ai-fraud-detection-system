FROM python:3.12

WORKDIR /app

COPY consumer/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY consumer/ .

CMD ["python", "transaction_consumer.py"]
