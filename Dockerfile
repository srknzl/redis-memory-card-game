FROM alpine:3.13.0

RUN apk add --no-cache python3 py3-pip

RUN pip3 install gunicorn==20.0.4 flask==1.1.2 redis==3.5.3 flask-cors==3.0.10

WORKDIR /opt/app

ADD api.py .

ENTRYPOINT [ "gunicorn", "-b", "127.0.0.1:3000", "--keyfile", "/opt/app/cert/privkey.pem", "--certfile", "/opt/app/cert/fullchain.pem", "api:app"]