HOSTNAME=`hostname`

sudo docker run \
  --name=bottlenecks-cadvisor-${HOSTNAME} \
  --volume=/:/rootfs:ro \
  --volume=/var/run:/var/run:rw \
  --volume=/sys:/sys:ro \
  --volume=/var/lib/docker/:/var/lib/docker:ro \
  --volume=/dev/disk/:/dev/disk:ro \
  --publish=8080:8080 \
  --detach=true \
  google/cadvisor:v0.25.0 \
  -storage_driver=Prometheus
