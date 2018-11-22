from CRC import crcCore

m = input()
g = input()

r = crcCore(int(m + '0' * (len(g) - 1), 2), int(g, 2))
trans = m + format(r, 'b').zfill(len(g) - 1)

ofn = 'transmitted_message.txt'
with open(ofn, 'w') as ofh:
    ofh.write(trans)

with open('g.txt', 'w') as gfh:
    gfh.write(g)

print(trans)

