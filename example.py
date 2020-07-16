#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import time

from dask_cloudprovider import FargateCluster
from distributed import Client

###############################################################################

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)4s: %(module)s:%(lineno)4s %(asctime)s] %(message)s",
)
log = logging.getLogger(__name__)

###############################################################################

def add_one(val: int) -> int:
    time.sleep(1)
    return val + 1

def multiply_by_ten(val: int) -> int:
    time.sleep(1)
    return val * 10


if __name__ == "__main__":
    # Cluster setup
    cluster = FargateCluster(
        image="jacksonmaxfield/fargate_example",
        worker_cpu=512,
        worker_mem=1024,
    )

    log.info(f"Dashboard available at: {cluster.dashboard_link}")
    cluster.adapt(minimum=10, maximum=30)
    client = Client(cluster.scheduler_address)

    # Actual work
    initial_values = list(range(1000))
    log.info(f"Values range: [{initial_values[0]}-{initial_values[-1]}]")

    # Add
    addition_futures = client.map(add_one, initial_values)
    values = client.gather(addition_futures)

    # Multiply
    multiplication_futures = client.map(multiply_by_ten, values)
    values = client.gather(multiplication_futures)

    # Results
    log.info(f"Values range: [{values[0]}-{values[-1]}]")

    # Manual shutdown of cluster
    cluster.close()
    client.close()

    log.info("All done!")
