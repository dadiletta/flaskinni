FROM tiangolo/uwsgi-nginx-flask:latest

RUN mkdir /app/flaskinni

COPY uwsgi.ini /app/

WORKDIR /app/flaskinni

ADD . .

ENV STATIC_PATH /app/flaskinni/static
ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD postgres
ENV POSTGRES_DB db
ENV DB_HOST 127.0.0.1

RUN pip install -r requirements.txt