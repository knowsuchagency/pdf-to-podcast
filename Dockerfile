FROM python:3.12-slim

RUN pip install uv
RUN uv venv

COPY requirements.txt .
RUN uv pip install -r requirements.txt

COPY . .

ENV GRADIO_SERVER_NAME="0.0.0.0"
ENV GRADIO_SERVER_PORT="8080"

CMD .venv/bin/granian --interface asgi --port 8080 --host 0.0.0.0  main:app
