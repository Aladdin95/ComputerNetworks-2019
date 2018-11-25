from Physical import *
from Protocol5 import *

client = physical_layer('client')
client.establish()
c_p5 = protocol5('client',client)

'''
for i in range(10):
    print(client.get().decode())
'''

'''
for i in range(10):
    client.send('elyeaaaaah')
'''
