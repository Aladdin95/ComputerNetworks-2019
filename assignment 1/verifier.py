from CRC import crcCore


t = input()

with open('g.txt', 'r') as ofh:
    g = ofh.read().strip()


if crcCore(int(t, 2), int(g, 2)) == 0:
    print('message is correct')
else:
    print('message is not correct')
