FROM alpine:3.13.0

RUN apk add --no-cache npm

WORKDIR /opt/app

ADD package.json .
ADD package-lock.json .
RUN npm i
ADD . .


RUN npm run build


ENTRYPOINT ["npm", "start"]