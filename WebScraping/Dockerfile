FROM python:3.6-alpine

RUN mkdir /app
WORKDIR /app

COPY requirements.txt requirements.txt
RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

COPY . .

LABEL maintainer="Max Dargatz <max.dargatz@de.ibm.com>"

CMD gunicorn -c gunicorn.py "hello.app:create_app()"
