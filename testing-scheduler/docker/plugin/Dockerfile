FROM java
MAINTAINER x-lab/Leo
RUN useradd -m noroot -s /bin/bash
USER noroot
WORKDIR /home/noroot
ENV BUILD_DIR build_dir
ENV REPO_DIR ${BUILD_DIR}/conductor
RUN sh -c 'mkdir -p ${BUILD_DIR}; cd ${BUILD_DIR}; git clone http://github.com/Netflix/conductor.git; cd conductor; git checkout v1.10.4'
RUN sh -c 'cd ${REPO_DIR}; ./gradlew build'

CMD tail -f /dev/null