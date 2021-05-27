FROM python:3.9-alpine AS base


FROM base as build

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.1.6

RUN apk add --no-cache \
    # Build/install dependencies
    gcc musl-dev \
    # For cryptography transitive Python dependency until PEP 656
    libffi-dev libressl-dev cargo \
    # For psycopg2 Python dependency until PEP 656
    postgresql-dev

RUN pip install "poetry==${POETRY_VERSION}"
RUN poetry config virtualenvs.in-project true

# Setup poetry
WORKDIR /poetry/
COPY poetry.lock pyproject.toml ./

RUN poetry install --no-dev -vvv


FROM base as final

RUN apk add --no-cache \
    postgresql-client

COPY --from=build /poetry/.venv/ /venv/
ENV PATH="/venv/bin:${PATH}"

WORKDIR /shortcake/
COPY . .

CMD ["python", "main.py"]
