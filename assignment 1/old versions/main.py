from Parser import parse
from CRC import crcCore


def alter(s, i):
    i -= 1
    t = '0'
    if s[i] == '0':
        t = '1'
    return s[0:i] + t + s[i+1:]


def generate(m, g):
    r = crcCore(int(m+'0'*(len(g)-1), 2), int(g, 2))
    return m+format(r,'b').zfill(len(g)-1)


def verify(t, g):
    if crcCore(int(t,2), int(g,2)) == 0:
        return 'message is correct'
    return 'message is not correct'


while True:
    cmd = input('write command like this\ngenerator < file.txt | alter 5 | verifier\nor press enter to exit\n')
    if len(cmd) == 0: break

    ret, file_name, index = parse(cmd)

    if ret == 0:
        print('invalid command, try again')
        continue

    with open(file_name, 'r') as handle:
        m = handle.readline().strip()
        g = handle.readline().strip()

    trans = generate(m, g)

    print(trans)
    print()

    ofn = 'transmitted_message.txt'
    with open(ofn, 'w') as ofh:
        ofh.write(trans)

    if index is not None:
        trans = alter(trans, index)

    print(verify(trans, g))
    print()
