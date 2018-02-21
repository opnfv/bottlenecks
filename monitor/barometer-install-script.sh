docker pull opnfv/barometer
sudo docker run  --name bottlenecks-barometer-server -tid --net=host -v `pwd`/../src/collectd_sample_configs:/opt/collectd/etc/collectd.conf.d \
-v /home/opnfv/bottlenecks/monitor/barometer-collectd.conf:/src/barometer/src/collectd/collectd/src/collectd.conf \
-v /var/run:/var/run -v /tmp:/tmp --privileged opnfv/barometer /run_collectd.sh
