FROM python:3.6-alpine

RUN mkdir /app
WORKDIR /app

COPY requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt --no-cache-dir && \
 python3 -m spacy download de_core_news_sm

COPY . .

LABEL maintainer="Max Dargatz <max.dargatz@de.ibm.com>"

CMD python3 webscraping.py
