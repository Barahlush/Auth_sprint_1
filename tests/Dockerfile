FROM python:3.10-alpine

WORKDIR /tests

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

RUN pip3 install --upgrade pip \
    &pip3 install -r requirements.txt --no-cache-dir

RUN ls
CMD python3 -m pytest
