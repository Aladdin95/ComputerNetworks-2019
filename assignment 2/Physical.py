import socket
import sys
import time
from threading import Timer


class physical_layer:

    def __init__(self, type):
        self.type = type
        self.soc = None
        self.address = None

    def establish(self, server_name='localhost', server_port=7777):
        init = '5'
        connected = False
        soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        if self.type == 'server':
            while not connected:
                soc.sendto(init.encode('UTF-8'), (server_name, server_port))
                m, address = soc.recvfrom(2048)
                if m.decode('UTF-8') != init:
                    connected = False
                else:
                    connected = True
            time.sleep(5)

        elif self.type == 'client':
            soc.bind(('', server_port))
            m, address = soc.recvfrom(2048)
            time.sleep(2)
            soc.sendto(m, address)
            connected = True

        else:
            return False

        self.soc = soc
        self.address = address
        return connected

    def send(self, frame):
        self.soc.sendto(str(frame).encode('UTF-8'), self.address)

    def get(self):
        return self.soc.recvfrom(2048)[0]
