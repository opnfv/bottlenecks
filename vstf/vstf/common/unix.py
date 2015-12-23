import os
import socket
from vstf.common import constants
from vstf.common import message


class UdpServer(object):
    def __init__(self):
        super(UdpServer, self).__init__()
        try:
            os.unlink(constants.sockaddr)
        except OSError:
            if os.path.exists(constants.sockaddr):
                raise Exception("socket not found %s" % constants.sockaddr)    
        self.conn=socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)    
    
    def listen(self,backlog=5):
        self.conn.listen(backlog)
        
    def accept(self):
        return self.conn.accept()
    
    def bind(self, addr=constants.sockaddr):
        return self.conn.bind(addr)
       
#     def send(self, data, addr):
#         return message.sendto(self.conn.sendto, data, addr)
        
#     def recv(self, size=constants.buff_size):
#         return message.recv(self.conn.recvfrom)
    
    def close(self):
        self.conn.close()


class UdpClient(object):
    def __init__(self):
        super(UdpClient, self).__init__()
        if not os.path.exists(constants.sockaddr):
            raise Exception("socket not found %s" % constants.sockaddr)    
        self.conn=socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
     
    def connect(self, addr=constants.sockaddr):
        return self.conn.connect(addr)
       
    def send(self, data):
        message.send(self.conn.send, data)
        
    def recv(self):
        return message.recv(self.conn.recv)
    
    def close(self):
        self.conn.close()