FROM tiangolo/meinheld-gunicorn-flask:python3.7-alpine3.8
RUN apk --update add bash nano
COPY ./requirements.txt /var/www/requirements.txt
RUN pip install -r /var/www/requirements.txt
