# Used to combine several different versions of the cdx.txt file in to 1 file with all unique entries from other files.
# Complete file from using this with my versions of cdx.txt and compressing is in /cdx/cdx.zip

inputFile1 = open("cdx_1.txt")
inputList1 = []
inputFile2 = open("cdx_2.txt")
inputList2 = []
inputFile3 = open("cdx_3.txt")
inputList3 = []
outputFile = open("cdx.txt", "w")
outputList = []

for i in inputFile1:
    inputList1.append(i)

for i in inputFile2:
    inputList2.append(i)

outputList = list(set(inputList1 + inputList2 + inputList3))

for i in outputList:
    outputFile.write(i)
