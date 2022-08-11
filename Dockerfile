# syntax=docker/dockerfile:1

FROM python:3.10.6-alpine3.15

WORKDIR /app
COPY "requirements.txt" "./"
COPY "gancio_requests-0.1.0.tar.gz" "./"
RUN pip install -r requirements.txt
RUN pip install gancio_requests-0.1.0.tar.gz

CMD ["python3", "src/bot.py"]
