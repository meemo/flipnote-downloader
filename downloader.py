import os
import time
import urllib.request
import sys

# Usage: downloader.py <delay in seconds (optional, defaults to 0)>

scriptStartTime = time.time()
sourceURL = "http://web.archive.org/cdx/search/cdx?matchType=prefix&url=jkz-dsidata.s3.amazonaws.com/kwz/"
downloadingDirectory = os.path.join(os.getcwd(), "kwz")
inputCDXList = []
delayInputValue = 0
filesDownloaded = 0
currentLine = 0

# Check if there was a delay value specified when running the script
if len(sys.argv) >= 2:
    if sys.argv[1].isnumeric() is True:
        delayInputValue = int(sys.argv[1])
    else:
        print("Delay value input is invalid, defaulting to 0 seconds.")
        delayInputValue = 0
else:
    delayInputValue = 0

# Print warnings
print("Warning: this script will take about a month to run completely and may get you IP banned from archive.org")
print("Errors are fairly normal, rerun the script and they will be automatically tried again.")
print("Please set a delay value wisely! Delay is currently set to " + str(delayInputValue) + " seconds.")
time.sleep(4)

if os.path.exists(os.path.join(downloadingDirectory)) is False:
    os.mkdir(os.path.join(downloadingDirectory))
if os.path.isfile("cdx.txt") is False:
    print("Existing cdx.txt file not found, downloading.")
    with urllib.request.urlopen(sourceURL) as response:
        if response.getcode() == 200:
            print("HTTP response good.")
            print("This may take a few minutes, do not close out the script.")
            inputCDXList = response.read().decode()
            outputCDXTextFile = open("cdx.txt", "w", newline="\n")
            outputCDXTextFile.writelines(inputCDXList)
            outputCDXTextFile.close()
            print("cdx.txt downloaded successfully.")
        else:
            # Request failed
            print("Connection to archive.org failed, please check your connection or try again later.")
            print("HTTP Response code: " + str(response.getcode()))
            exit()
else:
    print("Existing cdx.txt found!")
    inputCDXFile = open("cdx.txt")
    inputCDXList = inputCDXFile.readlines()
    inputCDXFile.close()

for i in inputCDXList:
    currentLine += 1
    processedURL = str("http://web.archive.org/web/" + str(str(i[84:])[:105]).replace(" ", "if_/"))
    # File name: characters 101 to 128, Author ID: characters 84 to 99
    fileName = processedURL[103:]
    authorID = str(processedURL[86:])[:-33]
    filePath = os.path.join(downloadingDirectory, authorID)
    if os.path.exists(filePath) is False:
        os.mkdir(filePath)
    if os.path.isfile(os.path.join(filePath, fileName)) is False:
        try:
            # Newer urls would fail to download properly, adding headers (below) forces it to download the right file.
            urlOpener = urllib.request.build_opener()
            urlOpener.addheaders = [('Content-type', 'application/octet-stream')]
            urllib.request.install_opener(urlOpener)
            urllib.request.urlretrieve(processedURL, os.path.join(filePath, fileName))
            filesDownloaded += 1
            print("Downloaded file #" + str(filesDownloaded) + " from: " + processedURL + ", line: " + str(currentLine))
        except Exception as errorException:
            print("Error on line " + str(currentLine) + ", url: " + processedURL + ", " + str(errorException))
            errorOutputFile = open("error.txt", "a", newline="\n")
            errorOutputFile.write("Line_" + str(currentLine) + "_URL_" + processedURL + "_Error_" + str(errorException))
            if os.path.isfile(os.path.join(filePath, fileName)) is True:
                os.remove(os.path.join(filePath, fileName))
                print("Deleted file created by error.")
                errorOutputFile.write("_Deleted" + "\n")
            else:
                errorOutputFile.write("\n")
            errorOutputFile.close()
    else:
        print("Duplicate on line: " + str(currentLine) + " URL: " + processedURL)
    time.sleep(delayInputValue)

print("Downloaded " + str(filesDownloaded) + " files in " + str(round(time.time() - scriptStartTime, 2)) + " seconds.")
