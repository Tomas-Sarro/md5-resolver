import sys

initial = int(sys.argv[1],16)
rotateBy = int(sys.argv[2])

rotatedCUT = f'{initial:08x}'

list = []
rotValue = []

def verify(test,during):

    result = int(test,16) >> rotateBy

    if (int(len(hex(result))) == 9 or int(len(hex(result))) == 10):
        list.append(hex(result))
        rotValue.append(test)

def paditUP():
    for i in range(0, 7):
        test = newTemp + '0'*i

        during = int(test,16) % 0xFFFFFFFF
        test = hex(int(test,16))

        if (hex(during) == hex(initial)):
            verify(test,during)
    
newTemp = rotatedCUT
for k in range(0,8):
    for x in range(0,len(rotatedCUT)):
        temp = newTemp
        
        if (k > 0):
            newTemp = str(k) + temp[1:] + temp[0]

        paditUP()
            
        for j in range(0,16):
            newTemp = newTemp[:-1] + str(hex(j)[2:])
            paditUP()
        
        newTemp = temp[1:] + temp[0]


sortedHexLast = sorted(list, key=lambda x: int(x[-1], 16))

flag = True
largestVal = []
for x in range(0, len(sortedHexLast)):
    reverse = len(sortedHexLast)-x-1
    tempVal = (sortedHexLast[reverse])[-1]
    if (flag):
        lastVal = tempVal
        flag = False
    if (lastVal == tempVal):
        largestVal.append(sortedHexLast[reverse])


largestVal = sorted(largestVal, key=lambda h: int(h, 16))
lastVal = largestVal[-1]

k = list.index(lastVal)
print(list[k] + "|" + rotValue[k])
