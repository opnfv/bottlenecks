##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from vstf.rpc_frame_work import rpc_producer


class EnvCollectApi(object):

    def __init__(self, rb_mq_server):
        """
        When use collect, a connection of rabbitmq is needed.
        """
        super(EnvCollectApi, self).__init__()
        if rb_mq_server is None:
            raise Exception("The connection of rabbitmq is None.")
        self.conn = rb_mq_server

    def collect_host_info(self, host):
        msg = self.conn.make_msg("collect_host_info")
        return self.conn.call(msg, host, timeout=2)

    def get_device_detail(self, host, nic_identity):
        msg = self.conn.make_msg("get_device_detail", identity=nic_identity)
        return self.conn.call(msg, host, timeout=2)

    def list_nic_devices(self, host):
        msg = self.conn.make_msg("list_nic_devices")
        return self.conn.call(msg, host, timeout=2)


if __name__ == "__main__":
    conn = rpc_producer.Server("192.168.188.10")
    c = EnvCollectApi(conn)
    print c.collect_host_info("local")
