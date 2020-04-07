FROM python:3.7-alpine

RUN mkdir /app
WORKDIR /app

RUN apk update
RUN apk add make automake gcc g++ subversion python3-dev

COPY requirements.txt requirements.txt
COPY WebScraping.py WebScraping.py

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps


LABEL maintainer="Max Dargatz"

CMD python WebScraping.py