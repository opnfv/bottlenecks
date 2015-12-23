import json
import uuid
import logging
import traceback
from vstf.common import constants

LOG = logging.getLogger(__name__)


def json_defaults(obj):
    if isinstance(obj, set):
        return list(obj)
    return "unknow obj"


def encode(msg):
    """obj to string"""
    if isinstance(msg, str):
        return msg
    else:
        return json.dumps(msg, default=json_defaults)


def decode(msg):
    """string to obj"""
    if isinstance(msg, str):
        return json.loads(msg)
    else:
        return msg


def gen_corrid():
    return str(uuid.uuid4())


def add_context(msg, **kwargs):
    return {'head': kwargs, 'body': msg}


def get_context(msg):
    if "head" in msg.iterkeys():
        return msg['head']
    else:
        return ""


def get_body(msg):
    if "body" in msg.iterkeys():
        return msg['body']
    else:
        return None


def get_corrid(context):
    """
    :param return: string of corrid or empty
    """
    if "corrid" in context.iterkeys():
        return context['corrid']
    else:
        return ""


def send(func, data):
    # the message must be a string
    if not isinstance(data, str):
        raise ValueError("the data must be a string")

    # the message's len must > 0
    msg_len = len(data)
    if msg_len <= 0:
        return True

    # the message's len must be less 999999999
    if len(str(msg_len)) > constants.MSG_FLAG_LEN:
        raise ValueError("the data's len too long")

    data = (constants.MSG_FLAG % (msg_len)) + data
    total_send = msg_len + constants.MSG_FLAG_LEN

    count = 0
    while count < total_send:
        sent = func(data[count:])
        if 0 == sent:
            raise RuntimeError("socket connection broken")
        count += sent

    return msg_len


def sendto(func, data, addr):
    # the message must be a string
    if not isinstance(data, str):
        raise ValueError("the data must be a string")

    # the message's len must > 0
    msg_len = len(data)
    if msg_len <= 0:
        return True

    # the message's len must be less 999999999
    if len(str(msg_len)) > constants.MSG_FLAG_LEN:
        raise ValueError("the data's len too long")

    data = (constants.MSG_FLAG % (msg_len)) + data
    total_send = msg_len + constants.MSG_FLAG_LEN

    count = 0
    while count < total_send:
        sent = func(data[count:], addr)
        if 0 == sent:
            raise RuntimeError("socket connection broken")
        count += sent

    return msg_len


def recv(func):
    head = func(constants.MSG_FLAG_LEN)
    # the FIN change to '' in python
    if head == '':
        raise RuntimeError("socket connection broken")

    if not head.isdigit():
        raise ValueError("the msg head is not a num.")

    msg_len = int(head)
    chunks = []
    count = 0
    while count < msg_len:
        chunk = func(min(msg_len - count, constants.buff_size))
        if chunk == '':
            raise RuntimeError("socket connection broken")
        chunks.append(chunk)
        count += len(chunk)

    return ''.join(chunks)


def dumpstrace():
    return traceback.format_exc()
