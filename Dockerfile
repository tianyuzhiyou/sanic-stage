FROM python:3.8.6-buster

ADD src /data/home

WORKDIR /data/home

RUN pip install --no-cache-dir --upgrade pip && pip install -r requirements.txt
