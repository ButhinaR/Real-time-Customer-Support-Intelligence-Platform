import datetime
from openlineage.client import OpenLineageClient
from openlineage.client.event_v2 import (
    RunEvent,
    RunState,
    Run,
    Job,
    InputDataset,
    OutputDataset,
)
from openlineage.client.uuid import generate_new_uuid
# Do NOT use OPENLINEAGE_DISABLED
lineage_client = OpenLineageClient()
run_id = str(generate_new_uuid())
job = Job(
    namespace="customer_support_capstone",
    name="twitter_to_delta_pipeline"
)
run = Run(
    runId=run_id
)
input_dataset = InputDataset(
    namespace="kafka://localhost:9092",
    name="customer_tickets"
)
output_dataset = OutputDataset(
    namespace="delta://content/delta",
    name="silver_tweets"
)
start_event = RunEvent(
    eventType=RunState.START,
    eventTime=datetime.datetime.utcnow().isoformat() + "Z",
    run=run,
    job=job,
    inputs=[input_dataset],
    outputs=[output_dataset],
    producer="customer-support-capstone",
    schemaURL="https://openlineage.io/spec/1-0-5/OpenLineage.json"
)
lineage_client.emit(start_event)

print("OpenLineage START event emitted.")
