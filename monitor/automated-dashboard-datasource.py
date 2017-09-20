import logging
import socket
import fcntl
import struct
import requests
from oslo_serialization import jsonutils


logger = logging.getLogger(__name__)


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


def _create_dashboard(ip, port, path):
    url = 'http://admin:admin@{}:{}/api/dashboards/db'.format(ip, port)
    print "Got IP!"
    with open(path) as f:
        data = jsonutils.load(f)
    try:
        post(url, {"dashboard": data})
        print "trying to post dashboard!"
        # print data
    except Exception:
        print "Create dashboard failed"
        raise


def _create_data_source(ip, port):
    url = 'http://admin:admin@{}:{}/api/datasources'.format(ip, port)
    print "got url for ds"
    data = {
        "name": "automated-ds",
        "type": "prometheus",
        "access": "direct",
        "url": "http://"+str(ip)+":9090",
    }
    try:
        post(url, data)
        print "trying to post ds"

    except Exception:
        print "Create datasources failed"
        raise


def post(url, data):
    data = jsonutils.dump_as_bytes(data)
    print "In post for dumping data"
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, data=data, headers=headers)
        result = response.json()
        logger.debug('The result is: %s', result)
        print "Trying to post"
        return result
    except Exception as e:
        print "failed post" + str(e)
        raise


_create_dashboard(get_ip_address('p1p3'), 3000, '/var/lib/grafana/' +
                  'dashboards/' +
                  'monitor-grafana-dashboards-prometheus-system_rev1.json')
_create_data_source(get_ip_address('p1p3'), 3000)
