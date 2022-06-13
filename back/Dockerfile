FROM python:3.9.1-slim-buster

ENV PYTHONUNBUFFERED 1

RUN python -m pip install --upgrade pip
RUN pip3 install gunicorn

WORKDIR /app
COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . ./

RUN pip3 install -e .
