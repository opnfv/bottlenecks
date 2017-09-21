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
    logger.info("Fetched IP for dashboard creation!")
    with open(path) as f:
        data = jsonutils.load(f)
    try:
        post(url, {"dashboard": data})
        logger.info( "Trying to post dashboard json!")
    except Exception:
        logger.info("Create dashboard failed")
        raise


def _create_data_source(ip, port):
    url = 'http://admin:admin@{}:{}/api/datasources'.format(ip, port)
    logger.info("Fetched URL for datasource")
    data = {
        "name": "automated-ds",
        "type": "prometheus",
        "access": "direct",
        "url": "http://{}:9090".format(ip),
    }
    try:
        post(url, data)
        logger.info("Trying to post datasource")

    except Exception:
        logger.info("Create Datasources failed")
        raise
                                                      

def post(url, data):
    data = jsonutils.dump_as_bytes(data)
    logger.info("In post method for dumping data")
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, data=data, headers=headers)
        result = response.json()
        logger.debug('The result is: %s', result)
        logger.info("Trying to post")
        return result
    except Exception as e:
        logger.info("Failed post" + str(e))
        raise


_create_dashboard(get_ip_address('ens5'), 3000, '/var/lib/grafana/' +
                  'dashboards/' +
                  'prometheus-system_rev1.json')
_create_data_source(get_ip_address('ens5'), 3000)
                                                                                                                                                                   70,1          Bot

