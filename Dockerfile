FROM python:3.12-slim

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock ./
RUN uv sync

COPY . .

CMD uv run uvicorn --host 0.0.0.0 --port 8000 main:app
