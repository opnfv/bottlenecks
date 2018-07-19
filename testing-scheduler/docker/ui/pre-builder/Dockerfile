FROM node:alpine
MAINTAINER x-lab/Leo
WORKDIR /home/testing-scheduler/ui
COPY ./ui .

RUN npm install
RUN npm run build

CMD tail -f /dev/null