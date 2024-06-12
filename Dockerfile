FROM python:3.12-slim

RUN pip install uv
RUN uv venv

COPY requirements.txt .
RUN uv pip install -r requirements.txt

COPY . .

CMD .venv/bin/granian --interface asgi --port 8080 --host 0.0.0.0  main:app
