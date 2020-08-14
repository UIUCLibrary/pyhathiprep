ARG PYTHON_VERSION=3.8
FROM python:${PYTHON_VERSION} as wheel_builder
ARG PIP_EXTRA_INDEX_URL
ARG PIP_TRUSTED_HOST
ARG PIP_INDEX_URL

RUN python -m pip install --upgrade pip &&  \
    pip install setuptools && \
    pip install wheel

RUN python -m pip install --upgrade pip && \
    pip install --upgrade setuptools && \
    pip install wheel

COPY requirements.txt requirements-dev.txt CI/docker/python/share/requirements-ci.txt /requirements/

RUN pip wheel --wheel-dir=/wheels \
        -r /requirements/requirements.txt \
        -r /requirements/requirements-dev.txt \
        -r /requirements/requirements-ci.txt && \
    rm -rf  /root/.cache

FROM python:${PYTHON_VERSION}
ARG USER_ID=1000
ARG GROUP_ID=1000

RUN groupadd -g $GROUP_ID user && \
    useradd -u $USER_ID -s /bin/sh -m -d /home/user -g user user

RUN apt update -y && apt install -y libgl1-mesa-glx

COPY --from=wheel_builder /wheels /wheels/
COPY requirements.txt requirements-dev.txt CI/docker/python/share/requirements-ci.txt /requirements/

RUN pip install --no-index --find-links=/wheels \
    -r /requirements/requirements.txt \
    -r /requirements/requirements-dev.txt \
    -r /requirements/requirements-ci.txt

ENV PIP_FIND_LINKS=/wheels
ENV PIP_NO_CACHE_DIR=1
USER user
WORKDIR /home/user