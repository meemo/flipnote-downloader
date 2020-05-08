import os.path
import shutil

workingDirectory = os.path.join(os.getcwd())

inputList = []

counterInteger = int(0)

if os.path.exists(os.path.join(workingDirectory, "download")) is False:
    os.mkdir(os.path.join(workingDirectory, "download"))
print("Made download folder")
inputFile = open("cdx.txt")
for i in inputFile:
    inputList.append(i)
inputFile.close()
print("Did cdx things")

for i in inputList:
    processedURL = str("http://web.archive.org/web/" + str(str(i[84:])[:105]).replace(" ", "/"))
    fileName = processedURL[100:]
    userID = str(processedURL[83:])[:-33]
    print("Modified input")
    # noinspection PyBroadException
    try:
        if os.path.exists(os.path.join(workingDirectory, "download", userID)) is False:
            os.mkdir(os.path.join(workingDirectory, "download", userID))
        shutil.move(os.path.join(workingDirectory, fileName[-3:], fileName),
                    os.path.join(workingDirectory, "download", userID, fileName))
        counterInteger = int(counterInteger + 1)
        print("Transferred " + str(counterInteger) + " of many")
    except Exception as e:
        print(e)
        pass


