FROM ubuntu:16.04

# General upgrades and requirements
RUN apt-get update && apt-get upgrade -y

# Install common build deps
RUN apt-get install -y \
    software-properties-common \
    build-essential            \
    cython

# Install and upgrade to py37
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update && apt-get install -y \
    python3.7     \
    python3.7-dev \
    python3-pip

# PIL / Pillow doesn't have a normal pip install on Ubuntu 16.04 must apt install
# This is required for Dask dashboard
RUN apt-get install -y \
    python3-pil

# Set python3.7 to default python3 and python
RUN ln -sf /usr/bin/python3.7 /usr/bin/python3
RUN ln -sf /usr/bin/python3.7 /usr/bin/python

# Set pip3 to default pip
RUN ln -sf /usr/bin/pip3 /usr/bin/pip

# Upgrade pip version
RUN pip install --upgrade pip

# Copy requirements and install
# Again, eventually this should be a python package install rather than a requirements
WORKDIR /dask-fargate-example/
COPY requirements.txt /dask-fargate-example/requirements.txt
RUN pip install -r requirements.txt
