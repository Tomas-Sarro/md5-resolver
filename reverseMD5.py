import subprocess
import math
import re

userInput = "e86fdc2283aff4717103f2d44d0610f7"

A = 0x67452301
B = 0xefcdab89
C = 0x98badcfe
D = 0x10325476

rotate_amounts = [
    7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
    5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
    4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
    6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21
]
constants = [int(abs(math.sin(i + 1)) * 2**32) & 0xFFFFFFFF for i in range(64)]

integer_value = int(userInput,16)
raw_bytes = integer_value.to_bytes(16,byteorder='big')
hex_string = '0x' + raw_bytes.hex()
byte_array = bytearray.fromhex(hex_string[2:])
final_hex_string = '0x' + byte_array[::-1].hex()


print(final_hex_string)

shifted_word3 = int(final_hex_string[:10],16)
shifted_word2 = int(final_hex_string[10:18],16)
shifted_word1 = int(final_hex_string[18:26],16)
shifted_word0 = int(final_hex_string[26:34],16)

print(hex(shifted_word0))
print(hex(shifted_word1))
print(hex(shifted_word2))
print(hex(shifted_word3))

a = '0xff' + hex((shifted_word0 - A) & 0xFFFFFFFF)[2:]
b = '0xff' + hex((shifted_word1 - B) & 0xFFFFFFFF)[2:]
c = '0xff' + hex((shifted_word2 - C) & 0xFFFFFFFF)[2:]
d = '0xff' + hex((shifted_word3 - D) & 0xFFFFFFFF)[2:]
new_b = '0x00000000'

if (len(a) == 11):
    a = a[:4] + '0' + a[4:]
if (len(b) == 11):
    b = b[:4] + '0' + b[4:]
if (len(c) == 11):
    c = c[:4] + '0' + c[4:]
if (len(d) == 11):
    d = d[:4] + '0' + d[4:]


for i in range(0,64):
    if (i > 0):
        b = new_b
    new_a, new_b,c,d = 0,c,d,a

    def printABCD():
        print("")
        print("i = ", 63-i)
        #print("rotAmount: ", rotAmount)
        #print("value: ", hex(value))
        print("to_rotate BEFORE: ", to_rotate_before)
        print("to_rotate AFTER: ", rotatedList)
        print("rotatedValue: ", rotatedValue)
        print("rotatedCUT: ", rotatedCUT)
        print("f: ", hex(f))
        print("a: ", a)
        print("b: ", new_b)
        print("c: ", c)
        print("d: ", d)
    
    if (int(b,16) < int(new_b,16)):
        b = b[:4] + 'f' + b[4:]

    rotatedCUT = hex(int(b,16) - int(new_b,16))
    
    if (len(rotatedCUT) > 10):
        rotatedCUT = '0x' + rotatedCUT[-8:]
    if (len(rotatedCUT) == 9):
        rotatedCUT = '0x0' + rotatedCUT[2:]

    rotAmount = rotate_amounts[63-i]

    rotatedList = subprocess.run(["python", "rotatedList.py", rotatedCUT, str(rotAmount)], capture_output=True, text=True)
    rotatedList = rotatedList.stdout
    rotatedList = rotatedList.strip()
    split_parts = rotatedList.split('|')

    print("rotatedList: ", split_parts[0])
    print("rotatedValue: ")
    print(split_parts[1])
    rotatedList = split_parts[0]
    rotatedValue = split_parts[1]
    
    def unAnd(backward):
        binaryHex = bin(backward)[2:]

        line = ''
        for x in binaryHex:
            if (x == '0'):
                line += str(0)
            if (x == '1'):
                line += str(1)

        after = hex(int(line,2))

    to_rotate_after = []

    this = hex(int(rotatedList,16))

    aDeduct = '0x0'
    if (len(this) == 9):
        this = this[:2] + "1" + this[-7:]
        aDeduct = '0x10000000'


    toRotateResult = subprocess.run(["python", "toRotate.py", this], capture_output=True, text=True)
    to_rotate_before = toRotateResult.stdout
    to_rotate_before = to_rotate_before.strip()

    iStr = str(63-i)
    fResult = subprocess.run(["python", "calculateF.py", new_b, c, d, to_rotate_before, iStr], capture_output=True, text=True)
    f = fResult.stdout
    f = int(f.strip(),16)

    if (f == "-"):
        f *= -1

    intR = int(this,16)
    value = 0

    with open('getValues.txt', 'r') as file:
        lines = file.readlines()
        line = lines[63-i]
        parts = line.strip().split(':')
    
        value = int(parts[1].strip(),16)

    file.close()


    testF = f
    if (i >= 16):
        aIntR = hex(intR)
        intR = '0x27' + aIntR[-8:]
        intR = int(intR,16)
        f = -f
        testF = int(hex(f)[-8:],16)

    newA = intR - int(testF) - constants[63-i] - value

    a = hex(newA)
    test = '0xff' + a[-8:]
    a = hex(int(test,16) - int(aDeduct,16))

    printABCD()


print("\n")
b = new_b
f = "0x" + hex(f)[4:]
a = "0x" + hex(int(a,16))[4:]
b = "0x" + hex(int(b,16))[4:]
c = "0x" + hex(int(c,16))[4:]
d = "0x" + hex(int(d,16))[4:]

if(f == hex(C)):
    print("f True: ", f)
else:
    print("f False: ", f)
    
if(a == hex(A)):
    print("a True: ", a)
else:
    print("a False: ", a)
    
if(b == hex(B)):
    print("b True: ", b)
else:
    print("b False: ", b)
    
if(c == hex(C)):
    print("c True: ", c)
else:
    print("c False: ", c)
    
if(d == hex(D)):
    print("d True: ", d)
else:
    print("d False: ", d)


