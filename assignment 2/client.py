from Physical import *

client = physical_layer('client')
client.establish()

for i in range(10):
    print(client.get().decode())

for i in range(10):
    client.send('elyeaaaaah')
