ARG PYTHON_VERSION=3.10
FROM python:${PYTHON_VERSION} as wheel_builder
ARG PIP_EXTRA_INDEX_URL
ARG PIP_TRUSTED_HOST
ARG PIP_INDEX_URL

RUN python -m pip install --upgrade pip &&  \
    pip install setuptools && \
    pip install wheel

COPY requirements.txt requirements-dev.txt requirements-ci.txt /requirements/

RUN pip wheel --wheel-dir=/wheels \
        -r /requirements/requirements.txt \
        -r /requirements/requirements-dev.txt \
        -r /requirements/requirements-ci.txt && \
    rm -rf  /root/.cache

FROM python:${PYTHON_VERSION}
RUN apt update -y && apt install -y libgl1-mesa-glx

COPY --from=wheel_builder /wheels /wheels/
COPY requirements.txt requirements-dev.txt requirements-ci.txt /requirements/

RUN pip install --no-index --find-links=/wheels \
    -r /requirements/requirements.txt \
    -r /requirements/requirements-dev.txt \
    -r /requirements/requirements-ci.txt

ENV PIP_FIND_LINKS=/wheels
ENV PIP_NO_CACHE_DIR=1

ENV SONAR_SCANNER_VERSION=4.7.0.2747
ARG SONAR_SCANNER_HOME=/opt/sonar/${SONAR_SCANNER_VERSION}-linux
ENV SONAR_USER_HOME=/opt/sonar/.sonar

RUN curl --create-dirs -sSLo /tmp/sonar-scanner.zip \
        https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-$SONAR_SCANNER_VERSION-linux.zip && \
    unzip -o /tmp/sonar-scanner.zip -d /opt/sonar/ && \
    rm /tmp/sonar-scanner.zip && \
    mkdir -p $SONAR_USER_HOME/cache && \
    chmod -R 777 "${SONAR_USER_HOME}" &&\
    ln -s /opt/sonar/sonar-scanner-$SONAR_SCANNER_VERSION-linux/bin/sonar-scanner /usr/local/bin/sonar-scanner && \
    which sonar-scanner

ENV PATH=$SONAR_SCANNER_HOME/bin:$PATH
ENV SONAR_SCANNER_OPTS="-server"
