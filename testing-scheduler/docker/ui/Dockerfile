FROM nginx
MAINTAINER x-lab/Leo

RUN rm /etc/nginx/conf.d/default.conf

ADD ./ui/config/default.conf /etc/nginx/conf.d/
COPY ./docker/ui/dist/  /usr/share/nginx/html/