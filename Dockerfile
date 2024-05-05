FROM python:3.11-slim as python-base

RUN pip install poetry==1.8.2

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /python_payment_service

COPY pyproject.toml poetry.lock ./
COPY python_payment_service ./python_payment_service

RUN touch README.md

RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

ENTRYPOINT ["poetry", "run", "uvicorn", "main:app", "--reload"]