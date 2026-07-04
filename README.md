#Program Name: MODERN RATA ENGINEERING FOR AI SYSTEMS – SADAIA ACADEMY
#Team Member: BUTHINA ALDHAFIAN (1075589604), RAZAN ASIRI()< HIND ALZAHRANI (1076306214).
# Real-Time Customer Support Intelligence Platform

This capstone project uses the Kaggle **Customer Support on Twitter** dataset to build an end-to-end customer support intelligence platform.

## Main Deliverables

1. **Ingestion Layer**
   - Real `confluent-kafka` Producer and Consumer.
   - Kafka topic: `customer_tickets`.
   - Strict schema validation with Pydantic.

2. **Delta Lakehouse**
   - Bronze, Silver, and Gold zones.
   - Real Delta Lake writes with `.format("delta")`.
   - Silver table uses Delta `MERGE`.

3. **RAG Pipeline**
   - Sentence chunking with overlap.
   - Embeddings using `BAAI/bge-small-en-v1.5`.
   - Qdrant vector index.
   - BM25 lexical search.
   - RRF hybrid fusion.
   - CrossEncoder reranking.

4. **Orchestration**
   - Airflow DAG with task dependency chain.

5. **Quality and Lineage**
   - Great Expectations validation suite.
   - OpenLineage client initialization.

## Important Colab Note

Google Colab does not reliably run long-lived Kafka/Redpanda broker processes.  
The included notebook therefore has a fallback path for the demo.  
The repository still contains the real `confluent-kafka` Producer and Consumer code required by the rubric.

## Run in Colab

Upload `Real_Time_Customer_Support_Capstone_Colab.ipynb` to Google Colab and run from top to bottom.

## Run Locally with Kafka/Redpanda

Example Redpanda Docker command:

```bash
docker run -d --name redpanda -p 9092:9092 \
docker.redpanda.com/redpandadata/redpanda:v24.1.2 \
redpanda start --overprovisioned --smp 1 --memory 1G
```

Then run the producer and consumer scripts.
