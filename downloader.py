import os.path
import time
import urllib.request
import zipfile

# Change the "0" here to change the delay (in seconds) between downloads
delayInputValue = 0

# Totals for file types
totalJPG = 237841
totalKWZ = 237841
totalTotal = 475682

# Print Warnings
print("Warning: this script will take at least a week to run completely and may get you IP banned from archive.org")
print("Please use a VPN and set a delay wisely!")
print("This script can be exited and continued from where you left off")
time.sleep(3)

inputCDXList = []
urlList = []
finishedList = []
jpgFileTotalCount = int(0)
kwzFileTotalCount = int(0)
workingDirectory = os.path.join(os.getcwd())

if os.path.exists(os.path.join(workingDirectory, "download")) is False:
    os.mkdir(os.path.join(workingDirectory, "download"))

# cdx.txt detection/creation
if os.path.isfile(os.path.join(workingDirectory, "cdx.txt")) is False:
    if os.path.isfile(os.path.join(workingDirectory, "cdx", "cdx.zip")) is True:
        print("Decompressing cdx.txt")
        with zipfile.ZipFile(os.path.join(workingDirectory, "cdx", "cdx.zip"), 'r') as zip_ref:
            zip_ref.extractall(os.path.join(workingDirectory))
    else:
        print("Downloading cdx.txt file")
        os.mkdir(os.path.join(workingDirectory, "cdx"))
        urllib.request.urlretrieve("https://archive.org/download/flipnote-hatena-archive/cdx.zip",
                                   os.path.join(workingDirectory, "cdx", "cdx.zip"))
        with zipfile.ZipFile(os.path.join(workingDirectory, "cdx", "cdx.zip"), 'r') as zip_ref:
            zip_ref.extractall(os.path.join(workingDirectory))
else:
    print("cdx.txt found!")
inputCDXFile = open(os.path.join(workingDirectory, "cdx.txt"))
for i in inputCDXFile:
    inputCDXList.append(i)
inputCDXFile.close()

if os.path.isfile(os.path.join(workingDirectory, "finished_urls.txt")) is True:
    finishedTextFile = open(os.path.join(workingDirectory, "finished_urls.txt"))
    for i in finishedTextFile:
        finishedList.append(i)
        if ".jpg" in i:
            jpgFileTotalCount = jpgFileTotalCount + 1
        elif ".kwz" in i:
            kwzFileTotalCount = kwzFileTotalCount + 1
    finishedTextFile.close()

for i in inputCDXList:
    processedURL = str("http://web.archive.org/web/" + str(str(i[84:])[:105]).replace(" ", "/"))
    # File name: characters 101 to 128
    fileName = processedURL[100:]
    # User ID: Characters 84 to 99
    userID = str(processedURL[83:])[:-33]
    if os.path.exists(os.path.join(workingDirectory, "download", userID)) is False:
        os.mkdir(os.path.join(workingDirectory, "download", userID))
    if os.path.isfile(os.path.join(workingDirectory, "download", userID, fileName)) is False:
        try:
            urllib.request.urlretrieve(processedURL, os.path.join(workingDirectory, "download", userID, fileName))
            print("Downloaded " + str(kwzFileTotalCount + jpgFileTotalCount + 1) + " of " + str(totalTotal) + " files.")
            outputLog = open(os.path.join(workingDirectory, "finished_urls.txt"), "w")
            outputLog.write("Downloaded: " + processedURL)
            outputLog.close()
            time.sleep(delayInputValue)
            if ".jpg" in fileName:
                jpgFileTotalCount = jpgFileTotalCount + 1
            elif ".kwz" in fileName:
                kwzFileTotalCount = kwzFileTotalCount + 1
        except Exception as errorException:
            print("Error on url: " + processedURL)
            print(errorException)
            errorFile = open(os.path.join(workingDirectory, "error.txt"), "w")
            errorFile.write("Error on url: " + processedURL)
            errorFile.write(str(errorException))
            errorFile.close()

    else:
        print("Skipped duplicate: " + processedURL)

print("Downloading complete!")
print(str(kwzFileTotalCount) + " of " + str(totalKWZ) + " .kwz files downloaded.")
print(str(jpgFileTotalCount) + " of " + str(totalJPG) + " .jpg files downloaded.")
print(str(kwzFileTotalCount + jpgFileTotalCount) + " files downloaded of " + str(totalTotal) + "‬ total.")
