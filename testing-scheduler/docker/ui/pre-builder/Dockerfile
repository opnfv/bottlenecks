FROM node:alpine
MAINTAINER Leo.C
WORKDIR /home/testing-scheduler/ui
COPY ./ui .

RUN /bin/sh -c 'npm config set registry https://registry.npm.taobao.org; npm install'
RUN /bin/sh -c 'npm run build'

CMD /bin/sh -c 'tail -f /dev/null'