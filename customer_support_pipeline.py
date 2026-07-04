from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def run_producer():
    from producer.kafka_producer import run_producer
    run_producer()

def run_validation():
    from validation.great_expectations_validation import run_validation
    run_validation()

def run_lakehouse():
    from lakehouse.delta_lakehouse import run_lakehouse
    run_lakehouse()

def run_rag():
    from rag.rag_pipeline import run_rag
    run_rag()

with DAG(
    "customer_support_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False
) as dag:

    ingest = PythonOperator(task_id="ingest", python_callable=run_producer)
    validate = PythonOperator(task_id="validate", python_callable=run_validation)
    lakehouse = PythonOperator(task_id="lakehouse", python_callable=run_lakehouse)
    rag = PythonOperator(task_id="rag", python_callable=run_rag)

    ingest >> validate >> lakehouse >> rag