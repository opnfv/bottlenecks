sudo docker rm -f t-scheduler-server \
                  t-scheduler-ui \
                  conductor_conductor-server_1 \
                  conductor_conductor-ui_1 \
                  conductor_dynomite_1 \
                  conductor_elasticsearch_1

sudo docker network rm conductor_default

sudo docker rmi x-lab/testing-scheduler:server \
                x-lab/testing-scheduler:ui \
                x-lab/conductor:builder \
                conductor:ui \
                conductor:server \
                elasticsearch:2.4 \
                v1r3n/dynomite:latest \
                java:8-jre-alpine \
                python:2.7 \
                node:alpine \
                nginx:latest \
                java:latest \

echo "--- Clean Finished ---"