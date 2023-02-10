FROM python:3.10-alpine

WORKDIR /tests

COPY tests/requirements.txt requirements.txt

RUN pip3 install -r requirements.txt --no-cache-dir

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY tests/ .

RUN ls
CMD python3 -m pytest
