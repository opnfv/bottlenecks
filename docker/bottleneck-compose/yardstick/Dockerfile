FROM opnfv/yardstick:stable

USER root

RUN apt-get update && apt-get install -y \
    openssh-server

# Create dir to put yardstick configure file
RUN mkdir /etc/yardstick
RUN mkdir /var/run/sshd

ADD conf/yardstick.conf /etc/yardstick/yardstick.conf

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
