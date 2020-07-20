#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import time
from typing import List

from dask_cloudprovider import FargateCluster
from distributed import Client
from prefect import Flow, task
from prefect.engine.executors import DaskExecutor

###############################################################################

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)4s: %(module)s:%(lineno)4s %(asctime)s] %(message)s",
)
log = logging.getLogger(__name__)

###############################################################################

@task
def add_one(val: int) -> int:
    time.sleep(1)
    return val + 1

@task
def multiply_by_ten(val: int) -> int:
    time.sleep(1)
    return val * 10

@task
def sort_values(values: List[int]) -> List[int]:
    return sorted(values)


if __name__ == "__main__":
    # Cluster setup
    cluster = FargateCluster(
        image="jacksonmaxfield/fargate_example",
        worker_cpu=512,
        worker_mem=1024,
    )

    log.info(f"Dashboard available at: {cluster.dashboard_link}")
    cluster.adapt(minimum=10, maximum=30)

    initial_values = list(range(1000))
    log.info(f"Values range: [{initial_values[0]}-{initial_values[-1]}]")

    # Generate the DAG
    with Flow("My Workflow") as flow:
        values = add_one.map(initial_values)
        values = multiply_by_ten.map(values)
        sort_values(values)

    # Run the Workflow / DAG
    state = flow.run(executor=DaskExecutor(address=cluster.scheduler_address))

    # Results
    # This returns all values that match the task name "sort_values"
    result_values = [
        state.result[flow_task].result for
        flow_task in flow.get_tasks(name="sort_values")
    ][0]  # since there is only one task with that name, return the first one

    log.info(f"Values range: [{result_values[0]}-{result_values[-1]}]")

    log.info("All done!")
