# Usage: downloader.py <delay in seconds (optional, defaults to 0)>

import os
import time
import urllib.request
import sys

if len(sys.argv) >= 2:
    if sys.argv[1].isnumeric() is True:
        delayInputValue = int(sys.argv[1])
    else:
        print("Delay value invalid, defaulting to 0 seconds.")
        delayInputValue = 0
else:
    delayInputValue = 0

startTime = time.time()
sourceURL = "http://web.archive.org/cdx/search/cdx?matchType=prefix&url=jkz-dsidata.s3.amazonaws.com/kwz/"
inputCDXList = []
kwzFileTotalCount = 0
jpgFileTotalCount = 0
linesProcessed = 0
workingDirectory = os.path.join(os.getcwd())

print("Warning: this script will take at least a week to run completely and may get you IP banned from archive.org")
print("Please use a VPN and set a delay wisely!")
time.sleep(3)

if os.path.exists(os.path.join(workingDirectory, "kwz")) is False:
    os.mkdir(os.path.join(workingDirectory, "kwz"))

if os.path.isfile("cdx.txt") is False:
    print("Existing cdx.txt file not found, downloading.")
    with urllib.request.urlopen(sourceURL) as response:
        if response.getcode() == 200:
            print("HTTP response good.")
            inputCDXList = response.read().decode()
            outputCDXTextFile = open("cdx.txt", "w", newline="\n")
            outputCDXTextFile.writelines(inputCDXList)
            outputCDXTextFile.close()
            print("cdx.txt created")
        else:
            print("Archive.org seems to be down, try again at some other time.")
            print("HTTP Response code: " + str(response.getcode()))
            exit()
else:
    print("Existing cdx.txt file found!")
    inputCDXFile = open("cdx.txt")
    inputCDXList = inputCDXFile.readlines()
    inputCDXFile.close()

for i in inputCDXList:
    linesProcessed += 1
    processedURL = str("http://web.archive.org/web/" + str(str(i[84:])[:105]).replace(" ", "/"))
    # File name: characters 101 to 128, User ID: Characters 84 to 99
    fileName = processedURL[100:]
    userID = str(processedURL[83:])[:-33]
    if os.path.exists(os.path.join(workingDirectory, "kwz", userID)) is False:
        os.mkdir(os.path.join(workingDirectory, "kwz", userID))
    if os.path.isfile(os.path.join(workingDirectory, "kwz", userID, fileName)) is False:
        try:
            urllib.request.urlretrieve(processedURL, os.path.join(workingDirectory, "kwz", userID, fileName))
            linesProcessed += 1
            if ".jpg" in fileName:
                jpgFileTotalCount += 1
            elif ".kwz" in fileName:
                kwzFileTotalCount += 1
            print("Downloaded new file #" + str(kwzFileTotalCount + jpgFileTotalCount) +
                  " from: " + processedURL)
            time.sleep(delayInputValue)
        except Exception as errorException:
            print("Error on line " + str(linesProcessed) + ", url: " + processedURL + ": " + str(errorException))
            errorOutputFile = open("error.txt", "a", newline="\n")
            errorOutputFile.write("Line_" + str(linesProcessed) + "_URL_" + processedURL
                                  + "_Error_" + str(errorException) + "\n")
            errorOutputFile.close()
    else:
        print("Duplicate on line: " + str(linesProcessed) + ", URL: " + processedURL)

print("Downloading completed in " + str(round(time.time() - startTime, 2)))
print(str(kwzFileTotalCount + jpgFileTotalCount) + " files downloaded total, " +
      str(kwzFileTotalCount) + " .kwz and " +
      str(jpgFileTotalCount) + " .jpg files.")
