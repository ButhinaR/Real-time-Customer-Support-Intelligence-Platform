"""
OpenLineage run lifecycle for the Customer Support Capstone.

This module emits real OpenLineage START and COMPLETE RunEvents.
Each event includes:
- InputDataset: Kafka topic customer_tickets
- OutputDataset: Delta table silver_tweets
"""

import datetime
from typing import Optional

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


PRODUCER = "customer-support-capstone"
SCHEMA_URL = "https://openlineage.io/spec/1-0-5/OpenLineage.json"


def build_lineage_objects(run_id: Optional[str] = None):
    """Create reusable OpenLineage run, job, input, and output objects."""
    run = Run(runId=run_id or str(generate_new_uuid()))

    job = Job(
        namespace="customer_support_capstone",
        name="twitter_to_delta_pipeline",
    )

    input_dataset = InputDataset(
        namespace="kafka://localhost:9092",
        name="customer_tickets",
    )

    output_dataset = OutputDataset(
        namespace="delta://content/delta",
        name="silver_tweets",
    )

    return run, job, input_dataset, output_dataset


def emit_start_event(lineage_client: OpenLineageClient, run, job, input_dataset, output_dataset):
    """Emit the START event before the pipeline runs."""
    start_event = RunEvent(
        eventType=RunState.START,
        eventTime=datetime.datetime.utcnow().isoformat() + "Z",
        run=run,
        job=job,
        inputs=[input_dataset],
        outputs=[output_dataset],
        producer=PRODUCER,
        schemaURL=SCHEMA_URL,
    )

    lineage_client.emit(start_event)
    print("OpenLineage START event emitted.")


def emit_complete_event(lineage_client: OpenLineageClient, run, job, input_dataset, output_dataset):
    """Emit the COMPLETE event after the pipeline finishes."""
    complete_event = RunEvent(
        eventType=RunState.COMPLETE,
        eventTime=datetime.datetime.utcnow().isoformat() + "Z",
        run=run,
        job=job,
        inputs=[input_dataset],
        outputs=[output_dataset],
        producer=PRODUCER,
        schemaURL=SCHEMA_URL,
    )

    lineage_client.emit(complete_event)
    print("OpenLineage COMPLETE event emitted.")


def demo_lifecycle():
    """
    Demo lifecycle emission.
    In the real pipeline, call emit_start_event before the pipeline work
    and emit_complete_event after the Delta table is written.
    """
    lineage_client = OpenLineageClient()
    run, job, input_dataset, output_dataset = build_lineage_objects()

    emit_start_event(lineage_client, run, job, input_dataset, output_dataset)
    # Pipeline work happens here.
    emit_complete_event(lineage_client, run, job, input_dataset, output_dataset)


if __name__ == "__main__":
    demo_lifecycle()
