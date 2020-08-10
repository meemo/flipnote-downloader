import os
import time
import urllib.request
import sys
import imghdr

# Usage: downloader.py [delay in seconds (optional, defaults to 0)]

scriptStartTime = time.time()
sourceURL = "http://web.archive.org/cdx/search/cdx?matchType=prefix&url=jkz-dsidata.s3.amazonaws.com/kwz/"
downloadingDirectory = os.path.join(os.getcwd(), "kwz")

inputCDXList = []
delayInputValue = 0
filesDownloaded = 0
currentLine = 0
errorCount = 0

urlOpener = urllib.request.build_opener()
urlOpener.addheaders = [('Content-type', 'application/octet-stream')]
urllib.request.install_opener(urlOpener)

if os.path.exists(os.path.join(downloadingDirectory)) is False:
    os.mkdir(os.path.join(downloadingDirectory))


def errorRecording(url, path, name, exception):
    global errorCount, currentLine
    errorCount += 1
    lineFilled = str(currentLine).zfill(6)
    print("Error occurred on line " + lineFilled + ", url: " + url + ", " + str(exception))
    errorOutputFile = open("error.txt", "a", newline="\n")
    errorOutputFile.write("Line_" + lineFilled + "_URL_" + url + "_Error_" + str(exception))
    if os.path.isfile(os.path.join(path, name)) is True:
        os.remove(os.path.join(path, name))
        print("Deleted error file.")
        errorOutputFile.write("_Deleted" + "\n")
    else:
        errorOutputFile.write("_No-Download" + "\n")
    errorOutputFile.close()


# Check for delay value specified
if len(sys.argv) >= 2:
    if sys.argv[1].isnumeric() is True:
        delayInputValue = int(sys.argv[1])
    else:
        print("Delay value input is invalid, defaulting to 0 seconds.")
        delayInputValue = 0
else:
    delayInputValue = 0

print("Warning: this script will take about a month to fully run.")
print("In that time, it is possible that your IP will blocked or banned from archive.org.")
print("Please set a delay value wisely! Delay is currently set to " + str(delayInputValue) + " seconds.")
time.sleep(3)

if os.path.isfile("cdx.txt") is False:
    print("Existing cdx.txt file not found, downloading.")
    with urllib.request.urlopen(sourceURL) as response:
        if response.getcode() == 200:
            print("This may take a few minutes, script is not frozen.")
            inputCDXList = response.read().decode()
            open("cdx.txt", "w", newline="\n").writelines(inputCDXList)
            print("cdx.txt file downloaded successfully.")
        else:
            # Request failed
            print("Connection to archive.org failed, please check your connection or try again later.")
            print("HTTP Response code: " + str(response.getcode()))
            exit()
else:
    print("Existing cdx.txt found!")
    inputCDXList = open("cdx.txt").readlines()

for i in inputCDXList:
    currentLine += 1
    # URL from CDX input: characters 84 to 189
    # File name: from URL, characters 103 to the end (135). Author ID: from URL, characters 86 to 102
    processedURL = str("http://web.archive.org/web/" + i[84:189].replace(" ", "if_/"))
    fileName = processedURL[103:]
    authorID = processedURL[86:102]
    filePath = os.path.join(downloadingDirectory, authorID)
    if os.path.exists(filePath) is False:
        os.mkdir(filePath)
    if os.path.isfile(os.path.join(filePath, fileName)) is False:
        try:
            urllib.request.urlretrieve(processedURL, os.path.join(filePath, fileName))
            # Check for 0 byte files
            if os.path.getsize(os.path.join(filePath, fileName)) == 0:
                errorRecording(processedURL, filePath, fileName, "0-Byte-File")
            # Valid kwz files always start with "KFH" when decoded to ansi.
            elif ".kwz" in fileName:
                if str(open(os.path.join(filePath, fileName), "rb").read().decode("ansi")).startswith("KFH") is False:
                    errorRecording(processedURL, filePath, fileName, "Invalid-KWZ")
            # Ensure jpg files are valid using imghdr
            elif ".jpg" in fileName:
                if imghdr.what(os.path.join(filePath, fileName)) != "jpeg":
                    errorRecording(processedURL, filePath, fileName, "Invalid-JPG")
            # File passed all checks.
            else:
                filesDownloaded += 1
                print("Downloaded file #" + str(filesDownloaded) + ". Line:", str(currentLine), "URL:", processedURL)
        except Exception as errorException:
            # General error catching from urllib.request
            errorRecording(processedURL, filePath, fileName, errorException)
    else:
        print("File already exists. Line: " + str(currentLine) + " URL: " + processedURL)
    time.sleep(delayInputValue)

print("Downloaded " + str(filesDownloaded) + " files in " + str(round(time.time() - scriptStartTime, 2)) + " seconds.")
print(str(errorCount) + " errors occurred.")
