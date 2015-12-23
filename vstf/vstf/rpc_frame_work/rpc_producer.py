#!/usr/bin/env python
# coding=utf-8
import uuid
import json
import time
import exceptions
import logging

import pika
from vstf.common import message
from vstf.common import excepts
from vstf.rpc_frame_work import constant

LOG = logging.getLogger(__name__)


class RpcProxy(object):
    def __init__(self, host,
                 user='guest',
                 passwd='guest',
                 port='5672'):
        """create a connection to rabbitmq,direct call and fan call supported.

        """
        # try to create connection of rabbitmq
        self._channel = None
        self._connection = None
        self._queue = str(uuid.uuid4())
        self._consume_tag = None

        self.user = user
        self.passwd = passwd
        self.srv = host
        self.port = port
        self.url = 'amqp://' + self.user + ':' + self.passwd + '@' + self.srv + ':' + self.port + '/%2F'
        try:
            self.connect(host, self.setup_vstf_producer)
        except Exception as e:
            LOG.error("create connection failed. e:%(e)s", {'e': e})
            raise e

        self.response = None
        self.corr_id = None

    def connect(self, host, ok_callback):
        """Create a Blocking connection to the rabbitmq-server
        
        :param str    host: the rabbitmq-server's host
        :param obj    ok_callback: if connect success than do this function
        
        """
        LOG.info("Connect to the server %s", host)
        self._connection = pika.BlockingConnection(pika.URLParameters(self.url))
        if self._connection:
            ok_callback()

    def setup_vstf_producer(self):
        self.open_channel()
        self.create_exchange(constant.exchange_d, constant.DIRECT)
        self.bind_queues()
        self.start_consumer()

    def open_channel(self):
        self._channel = self._connection.channel()
        if self._channel:
            self._channel.confirm_delivery()

    def create_exchange(self, name, type):
        LOG.info("Create %s exchange: %s", type, name)
        self._channel.exchange_declare(exchange=name, type=type)

    def bind_queues(self):
        LOG.info("Declare queue %s and bind it to exchange %s",
                 self._queue, constant.exchange_d)
        self._channel.queue_declare(queue=self._queue, exclusive=True)
        self._channel.queue_bind(exchange=constant.exchange_d, queue=self._queue)

    def start_consumer(self):
        LOG.info("Start response consumer")
        self._consume_tag = self._channel.basic_consume(self.on_response,
                                                        no_ack=True,
                                                        queue=self._queue)

    def stop_consuming(self):
        """Tell RabbitMQ that you would like to stop consuming by sending the
        Basic.Cancel RPC command.

        """
        if self._channel:
            LOG.info('Sending a Basic.Cancel RPC command to RabbitMQ')
            self._channel.basic_cancel(self._consume_tag)

        self.close_channel()

    def close_channel(self):
        """Call to close the channel with RabbitMQ cleanly by issuing the
        Channel.Close RPC command.

        """
        LOG.info('Closing the channel')
        self._channel.close()

    def close_connection(self):
        """This method closes the connection to RabbitMQ."""
        LOG.info('Closing connection')
        self._connection.close()

    def stop(self):
        self.stop_consuming()
        self.close_connection()

    def on_response(self, ch, method, props, body):
        """this func reciver the msg"""
        self.response = None
        if self.corr_id == props.correlation_id:
            self.response = json.loads(body)
            LOG.debug("Proxy producer reciver the msg: head:%(h)s, body:%(b)s",
                      {'h': self.response.get('head'), 'b': self.response.get('body')})
        else:
            LOG.warn("Proxy producer Drop the msg "
                     "because of the wrong correlation id, %s\n" % body)

    def publish(self, target, corrid, body):
        properties = pika.BasicProperties(reply_to=self._queue,
                                          correlation_id=corrid)
        LOG.debug("start to publish message to the exchange=%s, target=%s, msg=%s"
                  , constant.exchange_d, target, body)
        return self._channel.basic_publish(exchange=constant.exchange_d,
                                           routing_key=target,
                                           mandatory=True,
                                           properties=properties,
                                           body=message.encode(body))

    def call(self, msg, target='agent', timeout=constant.TIMEOUT):
        """send msg to agent by id, this func will wait ack until timeout
        :msg the msg to be sent
        :id agent's id
        :timeout timeout of waiting response

        """
        self.response = None
        queue = constant.queue_common + target
        # the msg request and respone must be match by corr_id
        self.corr_id = str(uuid.uuid4())
        # same msg format 
        msg = message.add_context(msg, corrid=self.corr_id)

        # send msg to the queue
        try:
            ret = self.publish(queue, self.corr_id, msg)
        except Exception as e:
            LOG.error(message.dumpstrace())
            raise excepts.ChannelDie

        # if delivery msg failed. return error
        # clean the msg in the queue
        if not ret:
            LOG.error("productor message delivery failed.")
            return "Message can not be deliveryed, please check the connection of agent."

        # wait for response
        t_begin = time.time()
        while self.response is None:
            self._connection.process_data_events()
            count = time.time() - t_begin
            if count > timeout:
                LOG.error("Command timeout!")
                # flush the msg of the queue
                self._channel.queue_purge(queue=queue)
                # self.channel.basic_cancel()
                return False

        msg_body = message.get_body(message.decode(self.response))

        # deal with exceptions
        if msg_body \
                and isinstance(msg_body, dict) \
                and msg_body.has_key('exception'):
            ename = str(msg_body['exception'].get('name'))
            if hasattr(exceptions, ename):
                e = getattr(exceptions, ename)()
            else:
                class CallError(Exception):
                    pass

                e = CallError()
            e.message = str(msg_body['exception'].get('message'))
            e.args = msg_body['exception'].get('args')
            raise e
        else:
            return msg_body


class Server(object):
    def __init__(self, host=None,
                 user='guest',
                 passwd='guest',
                 port='5672'):
        super(Server, self).__init__()
        # Default use salt's master ip as rabbit rpc server ip
        if host is None:
            raise Exception("Can not create rpc proxy because of the None rabbitmq server address.")

        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        try:
            self.proxy = RpcProxy(host=host,
                                  port=port,
                                  user=user,
                                  passwd=passwd)
        except Exception as e:
            raise e

    def call(self, msg, msg_id, timeout=constant.TIMEOUT):
        """when you add a server listen to the rabbit
        you must appoint which queue to be listen.
        :@queue the queue name.
        """
        retry = False

        try:
            ret = self.proxy.call(msg, target=msg_id, timeout=timeout)
        except excepts.ChannelDie:
            # this may be the proxy die, try to reconnect to the rabbit
            del self.proxy
            self.proxy = RpcProxy(host=self.host,
                                  port=self.port,
                                  user=self.user,
                                  passwd=self.passwd)
            if self.proxy is None:
                raise excepts.UnsolvableExit
            retry = True

        if retry:
            # if retry happened except, throw to uplay
            ret = self.proxy.call(msg, target=msg_id, timeout=timeout)

        return ret

    def cast(self, msg):
        """when you want to send msg to all agent and no reply, use this func"""
        LOG.warn("cast not support now.")

    def make_msg(self, method, **kargs):
        return {'method': method,
                'args': kargs}

    def close(self):
        self.proxy.stop()
