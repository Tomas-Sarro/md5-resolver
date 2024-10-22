# Takes b, c, and d to calculate f

import sys

b = int(sys.argv[1],16)
c = int(sys.argv[2],16)
d = int(sys.argv[3],16)
isNeg = (sys.argv[4])[0]
i = int(sys.argv[5])

if (0 <= i <= 15):
    f = bin((b & c)|(~b & d))
    
if (16 <= i <= 31):
    f = bin((d & b)|(~d & c))

if (32 <= i <= 47):
    f = bin(b ^ c ^ d)
    
if (48 <= i <= 63):
    f = bin(c ^ (b | ~d))

if (isNeg[0] == "-"):
    f = f[3:]
    f = int(f,2)
    f = "-" + hex(f)
    print(f)
else:
    f = f[1:]
    f = int(f,2)
    print(f)

