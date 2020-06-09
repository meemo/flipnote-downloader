inputFile1 = open("cdx_1.txt")
inputFile2 = open("cdx_2.txt")
outputFile = open("cdx.txt", "w")

inputList1 = []
inputList2 = []
outputList = []

for i in inputFile1:
    inputList1.append(i)

for i in inputFile2:
    inputList2.append(i)

outputList = list(set(inputList1 + inputList2))

for i in outputList:
    outputFile.write(i)
