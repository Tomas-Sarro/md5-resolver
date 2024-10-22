# accepts input and tries to return the correct answer

import sys

after = int(sys.argv[1],16)

arr = []
def function(after):
    
    if len(hex(after)) > 10:
        result_hex = '0x' + hex(after)[-8:]
        after = int(result_hex,16)

    binAfter = bin(after)

    def reverseBit(line):
        line = format(int(line,2) - int("1",2), '0' + str(len(line)) + 'b')

        string = ''
        for x in line:
            if (x == "0"):
                string+="1"
            else:
                string+="0"

        string = '-0b' + string[3:]
        before = "-" + hex(int(string,2))[2:]
        return(before)

    def negativeReturn():
        return(reverseBit('000'+binAfter[3:]))

    def takeFirst(test):
        k = 0
        if (len(test[2:]) < 8):
            k = 1
        
        for i in range(0,16):
            hexI = hex(i)[2:]
            here = test[3-k:]
            here = '-0x' + str(hexI) + here
            if (hex(after) == verifyHex(here)):
                return(here)
                
    def verifyHex(work):
        result = int(bin(int(work,16) & 0xFFFFFFFF),2)
        return(hex(result))

    test = takeFirst(negativeReturn())

    try:
        if (test[3] == "0"):
            test = test[:3] + test[4:]
    except TypeError:
        function(after - int('0x10000000',16))
        function(after + int('0x10000000',16))
        
    arr.append(test)
    print(test)

function(after)
arr = arr[:-1]

int_values = [int(x, 16) for x in arr]
average = (int_values[0] + int_values[1]) // 2
average_hex = hex(average)
print(average_hex)
