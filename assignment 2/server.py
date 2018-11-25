from Physical import *
from Protocol5 import *

server = physical_layer('server')
server.establish()
s_p5 = protocol5('server',server)
'''
for i in range(10):
    server.send('edrb ya badry')
'''
'''
for i in range(10):
    print(server.get().decode())
'''
