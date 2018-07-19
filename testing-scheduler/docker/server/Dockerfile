FROM python:2.7
MAINTAINER Leo.C
WORKDIR /home/testing-scheduler/server
COPY ./server .

RUN pip install -r ./python_modules.txt
EXPOSE 5310
CMD sh -c 'python ./src/rest/router.py'
