FROM python:3.8

# Instala o cliente Docker
RUN apt-get update && \
    apt-get install -y docker.io && \
    apt-get install -y build-essential

RUN pip3 install mysqlclient && \
    pip install --upgrade pip

WORKDIR /app
