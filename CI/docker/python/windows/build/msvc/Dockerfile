# escape=`
ARG CERTS_GENERATOR_IMAGE=mcr.microsoft.com/dotnet/framework/sdk:4.8
ARG PYTHON_DOCKER_IMAGE_BASE=python:3.7

FROM ${CERTS_GENERATOR_IMAGE} as certsgen
RUN certutil -generateSSTFromWU roots.sst

FROM ${PYTHON_DOCKER_IMAGE_BASE} as wheel_builder
ARG PIP_EXTRA_INDEX_URL
ARG PIP_TRUSTED_HOST
ARG PIP_INDEX_URL
RUN python -m pip install pip --upgrade ; `
    pip install wheel ; `
    pip install setuptools --upgrade

COPY requirements.txt requirements-dev.txt requirements-freeze.txt CI/docker/python/share/requirements-ci.txt c:/temp/
RUN pip wheel -w c:/wheels `
    -r c:/temp/requirements.txt `
    -r c:/temp/requirements-dev.txt `
    -r c:/temp/requirements-freeze.txt `
    -r c:/temp/requirements-ci.txt

FROM ${PYTHON_DOCKER_IMAGE_BASE}
COPY --from=certsgen c:/roots.sst roots.sst
RUN certutil -addstore -f root roots.sst ; `
    del roots.sst


RUN python -m pip install pip --upgrade ; pip install wheel ; pip install setuptools --upgrade
COPY --from=wheel_builder c:/wheels c:/wheels/
COPY requirements.txt requirements-dev.txt requirements-freeze.txt CI/docker/python/share/requirements-ci.txt c:/temp/
RUN python -m pip install --no-index --find-links c:/wheels `
    -r c:\temp\requirements.txt `
    -r c:\temp\requirements-dev.txt `
    -r c:\temp\requirements-freeze.txt `
    -r c:/temp/requirements-ci.txt

