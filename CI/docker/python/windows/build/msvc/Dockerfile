# escape=`
ARG CERTS_GENERATOR_IMAGE=mcr.microsoft.com/dotnet/framework/sdk:4.8
ARG PYTHON_DOCKER_IMAGE_BASE=python:3.7

FROM ${CERTS_GENERATOR_IMAGE} as certsgen
RUN certutil -generateSSTFromWU roots.sst

FROM ${PYTHON_DOCKER_IMAGE_BASE}
COPY --from=certsgen c:/roots.sst roots.sst
RUN certutil -addstore -f root roots.sst ; `
    del roots.sst

ADD requirements.txt requirements-freeze.txt requirements-dev.txt c:/temp/

RUN python -m pip install pip --upgrade ; python -m pip install -r c:\temp\requirements.txt -r c:\temp\requirements-dev.txt -r c:\temp\requirements-freeze.txt coverage flake8 lxml
RUN python -m pip install setuptools --upgrade
RUN pip install devpi-client
