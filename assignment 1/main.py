from Parser import parse
from CRC import crcCore


def alter(s, i):
    i -= 1
    t = '0'
    if s[i] == '0':
        t = '1'
    return s[0:i] + t + s[i+1:]


def generate(m, g):
    r = crcCore(int(m+'0'*len(g), 2), int(g, 2))
    rstr = format(r, 'b').zfill(len(g))
    return m+rstr


def verify(t, g):
    if crcCore(int(t,2), int(g,2)) == 0:
        return 'message is correct'
    return 'message is not correct'
