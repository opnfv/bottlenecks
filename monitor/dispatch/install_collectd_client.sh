MONITOR_CONFIG="/etc/collectd_config"
HOSTNAME=`hostname`

sudo docker run --name bottlenecks-collectd-${HOSTNAME} -d \
  --privileged \
  -v ${MONITOR_CONFIG}/collectd_client.conf:/etc/collectd/collectd.conf:ro \
  -v /proc:/mnt/proc:ro \
  fr3nd/collectd:5.5.0-1
