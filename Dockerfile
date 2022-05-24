FROM tiangolo/meinheld-gunicorn-flask:latest

RUN mkdir /flaskinni

WORKDIR /flaskinni

ADD . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install --no-cache-dir -U meinheld