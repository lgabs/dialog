# 
# Base stage - define env vars
# 
FROM python:3.11-slim as python-base

ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # poetry
    POETRY_VERSION=1.6.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false
    
ENV PATH="$POETRY_HOME/bin:$PATH"

RUN pip install poetry==$POETRY_VERSION
WORKDIR /app
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-root

COPY ./src ./src
RUN poetry install --only-root
CMD "/app/src/scripts/start_web_server.sh"