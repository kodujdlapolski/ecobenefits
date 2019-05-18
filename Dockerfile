FROM python:3.6-slim-stretch
COPY . /app/
WORKDIR /app
RUN apt-get update && apt-get install -y gcc make libpq-dev
RUN python3 -m pip install -r requirements.txt