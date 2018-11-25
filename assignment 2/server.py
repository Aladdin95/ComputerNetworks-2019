from Physical import *


server = physical_layer('server')
server.establish()
for i in range(10):
    server.send('edrb ya badry')

for i in range(10):
    print(server.get().decode())
