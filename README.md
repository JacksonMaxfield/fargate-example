# Dask + Prefect + Fargate Example

## Quick Start
(Preferably in a Python environment)

```bash
pip install -r requirements.txt
python prefect_example.py
```

## Dev Explaination

Here is a video of me explaining the repo and how things work:
[YouTube](https://youtu.be/4YroVZuHgcQ)

### Changelog since Recording

* Added a [Prefect](https://github.com/prefecthq/prefect) version of the workflow
* Fixed the bug with cluster shutdown
* Consolidated the various Docker build, run, and push files to a single Makefile

## Other Commands

* `make docker-build`, build the docker image
* `make docker-push`, push the local docker image to dockerhub
* `make docker-local`, start a docker container w/ the local image
