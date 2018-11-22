import sys
s = input()
i = int(sys.argv[1]) - 1

t = '0'
if s[i] == '0':
    t = '1'
print(s[0:i] + t + s[i + 1:])
