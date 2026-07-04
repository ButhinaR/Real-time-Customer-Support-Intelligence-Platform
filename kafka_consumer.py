import json
import pandas as pd
from confluent_kafka import Consumer
from schema import Tweet

KAFKA_BOOTSTRAP = "localhost:9092"
KAFKA_TOPIC = "customer_tickets"

def run_consumer(max_empty_polls: int = 10):
    consumer = Consumer({
        "bootstrap.servers": KAFKA_BOOTSTRAP,
        "group.id": "support-group",
        "auto.offset.reset": "earliest"
    })

    consumer.subscribe([KAFKA_TOPIC])

    records = []
    empty_polls = 0

    while empty_polls < max_empty_polls:
        msg = consumer.poll(1)

        if msg is None:
            empty_polls += 1
            continue

        empty_polls = 0

        if msg.error():
            print("Kafka error:", msg.error())
            continue

        data = json.loads(msg.value().decode("utf-8"))

        try:
            tweet = Tweet(**data)
            records.append(tweet.model_dump())
        except Exception as exc:
            print("Validation error:", exc)

    consumer.close()

    out_path = "data/silver/validated_tweets.csv"
    pd.DataFrame(records).to_csv(out_path, index=False)
    print(f"Consumed and validated {len(records)} records.")

if __name__ == "__main__":
    run_consumer()