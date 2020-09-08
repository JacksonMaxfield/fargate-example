###############################################################################
# Tasks in Makefile
.PHONY: docker-build docker-push docker-local
.DEFAULT_GOAL := help

###############################################################################
# Help display setup
define BROWSER_PYSCRIPT
import os, webbrowser, sys

try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

###############################################################################
# Variables
DOCKER_IMAGE_NAME := jacksonmaxfield/fargate_example

###############################################################################
# Tasks

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

docker-build:  ## build the docker image
	docker build -t $(DOCKER_IMAGE_NAME) .

docker-push:  ## push the docker image to dockerhub
	docker push $(DOCKER_IMAGE_NAME)

docker-local:  ## spawn a bash session inside the docker image
	docker run --rm -it $(DOCKER_IMAGE_NAME) bash
