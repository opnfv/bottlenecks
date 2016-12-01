FROM opnfv/bottlenecks:latest

USER root

RUN apt-get update && apt-get install -y \
    openssh-server

RUN mkdir /var/run/sshd
EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
