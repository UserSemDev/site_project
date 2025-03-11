FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    curl -sSL https://install.python-poetry.org/ | python3 - && \
    apt-get remove -y curl && \
    rm -rf /var/lib/apt/lists/*

ENV PATH="${PATH}:/root/.local/bin"

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-interaction --no-ansi

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]