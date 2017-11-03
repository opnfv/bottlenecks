MONITOR_CONFIG="/root/collectd-config"

# Collectd
sudo docker run --name bottlenecks-automated-collectd -d \
  --privileged \
  -v ${MONITOR_CONFIG}:/etc/collectd:ro \
  -v /proc:/mnt/proc:ro \
  fr3nd/collectd

