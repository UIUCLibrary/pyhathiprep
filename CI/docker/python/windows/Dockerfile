# escape=`
ARG CERTS_GENERATOR_IMAGE=mcr.microsoft.com/dotnet/framework/sdk:4.8
ARG PYTHON_VERSION=3.7

FROM ${CERTS_GENERATOR_IMAGE} as certsgen
RUN certutil -generateSSTFromWU roots.sst

FROM python:${PYTHON_VERSION} as wheel_builder
ENV PIP_NO_CACHE_DIR=1
ARG PIP_EXTRA_INDEX_URL
ARG PIP_TRUSTED_HOST
ARG PIP_INDEX_URL
COPY requirements.txt requirements-dev.txt requirements-freeze.txt CI/docker/python/share/requirements-ci.txt c:/temp/
RUN python -m pip install pip --upgrade ; `
    pip install wheel ; `
    pip install setuptools --upgrade ; `
    pip wheel -w c:/wheels `
        -r c:/temp/requirements.txt `
        -r c:/temp/requirements-dev.txt `
        -r c:/temp/requirements-freeze.txt `
        -r c:/temp/requirements-ci.txt

FROM python:${PYTHON_VERSION}
COPY --from=certsgen c:/roots.sst roots.sst
RUN certutil -addstore -f root roots.sst ; `
    del roots.sst

ENV PIP_NO_CACHE_DIR=1
COPY --from=wheel_builder c:/wheels c:/wheels/
COPY requirements.txt requirements-dev.txt requirements-freeze.txt CI/docker/python/share/requirements-ci.txt c:/temp/
RUN python -m pip install pip --upgrade ; `
    pip install wheel ; pip install setuptools --upgrade ; `
    python -m pip install --no-index --find-links c:/wheels `
        -r c:\temp\requirements.txt `
        -r c:\temp\requirements-dev.txt `
        -r c:\temp\requirements-freeze.txt `
        -r c:/temp/requirements-ci.txt

ENV PIP_FIND_LINKS=c:/wheels/
