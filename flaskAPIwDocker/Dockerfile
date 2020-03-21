FROM python:3.6-alpine

RUN mkdir /app
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

LABEL maintainer="Max Dargatz <max.dargatz@de.ibm.com>"

CMD gunicorn -c gunicorn.py "hello.app:create_app()"
