import os
from openlineage.client import OpenLineageClient

def init_lineage():
    os.environ["OPENLINEAGE_DISABLED"] = "true"
    client = OpenLineageClient()
    print("OpenLineage client initialized.")
    return client

if __name__ == "__main__":
    init_lineage()