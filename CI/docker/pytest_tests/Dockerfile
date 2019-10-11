FROM python:3.7

ADD ["requirements.txt", "requirements-dev.txt", "./"]
RUN pip install --no-cache-dir \
    "tox<3.10" \
    pytest \
    pytest-bdd \
    bandit \
    mypy \
    flake8 \
    coverage \
    pylint \
     -r requirements.txt \
     -r requirements-dev.txt