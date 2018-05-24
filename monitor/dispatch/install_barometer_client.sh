HOSTNAME=`hostname`

docker pull opnfv/barometer
sudo docker run  --name bottlenecks-barometer-${HOSTNAME} -d --net=host \
  -v /etc/barometer_config/barometer_client.conf:/src/barometer/src/collectd/collectd/src/collectd.conf \
  -v /etc/barometer_config/barometer_client.conf:/opt/collectd/etc/collectd.conf \
  -v /var/run:/var/run -v /tmp:/tmp \
  --privileged opnfv/barometer /run_collectd.sh