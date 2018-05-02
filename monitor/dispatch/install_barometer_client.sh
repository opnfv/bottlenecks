docker pull opnfv/barometer
sudo docker run  --name bottlenecks-barometer-client -tid --net=host \
  -v `pwd`/../src/collectd_sample_configs:/opt/collectd/etc/collectd.conf.d \
  -v /etc/barometer_config/barometer_client_collectd.conf:/src/barometer/src/collectd/collectd/src/collectd.conf \
  -v /etc/barometer_config/barometer_client_collectd.conf:/opt/collectd/etc/collectd.conf \
  -v /var/run:/var/run \
  -v /tmp:/tmp \
  --privileged opnfv/barometer /run_collectd.sh
