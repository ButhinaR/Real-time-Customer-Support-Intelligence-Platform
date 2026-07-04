import json
import pandas as pd
from confluent_kafka import Producer

KAFKA_BOOTSTRAP = "localhost:9092"
KAFKA_TOPIC = "customer_tickets"

def run_producer(csv_path: str = "data/raw/twcs.csv", limit: int = 5000):
    df = pd.read_csv(csv_path)
    tweets = df[["tweet_id", "author_id", "text", "created_at"]].dropna().head(limit)

    producer = Producer({"bootstrap.servers": KAFKA_BOOTSTRAP})

    for _, row in tweets.iterrows():
        event = {
            "tweet_id": int(row["tweet_id"]),
            "author_id": str(row["author_id"]),
            "text": str(row["text"]),
            "created_at": str(row["created_at"])
        }

        producer.produce(KAFKA_TOPIC, json.dumps(event).encode("utf-8"))

    producer.flush()
    print(f"Produced {len(tweets)} messages to {KAFKA_TOPIC}")

if __name__ == "__main__":
    run_producer()