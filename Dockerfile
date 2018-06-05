FROM python:3.6-alpine

MAINTAINER jhunthrop@gmail.com

RUN apk add --update g++ make && rm -r /var/cache

COPY . /opt/zapier-fun

WORKDIR /opt/zapier-fun

RUN pip install . gunicorn

CMD ["gunicorn", "zapier_fun.app:app", "--bind", "0.0.0.0:80", "--worker-class", "sanic.worker.GunicornWorker"]
