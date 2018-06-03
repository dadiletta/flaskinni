FROM tiangolo/uwsgi-nginx-flask:python3.6

RUN mkdir /app/flaskinni

COPY uwsgi.ini /app/

WORKDIR /app/flaskinni

ADD . .

ENV STATIC_PATH /app/flaskinni/static

RUN pip install -r requirements.txt