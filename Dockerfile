# syntax=docker/dockerfile:1
FROM ubuntu:22.04
FROM python:3.10.6-buster

WORKDIR /app
COPY "requirements.txt" "./"
RUN pip install -r requirements.txt

CMD ["python3", "-m", "gancio_telegram_bot"]