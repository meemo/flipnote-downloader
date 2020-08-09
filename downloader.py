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

urlOpener = urllib.request.build_opener()
urlOpener.addheaders = [('Content-type', 'application/octet-stream')]
urllib.request.install_opener(urlOpener)

if os.path.exists(os.path.join(downloadingDirectory)) is False:
    os.mkdir(os.path.join(downloadingDirectory))


def writeError(url, path, name):
    print("Downloaded an invalid file: " + fileName)
    open("error_files_deleted.txt", "a", newline="\n").write(processedURL + "\n")
    os.remove(os.path.join(filePath, fileName))
    print("Deleted invalid file.")


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
                writeError(processedURL, filePath, fileName)
            # Valid kwz files always start with "KFH" when decoded to ansi.
            elif ".kwz" in fileName:
                if str(open(os.path.join(filePath, fileName), "rb").read().decode("ansi")).startswith("KFH") is False:
                    writeError(processedURL, filePath, fileName)
            # Ensure jpg files are valid using imghdr
            elif ".jpg" in fileName:
                if imghdr.what(os.path.join(filePath, fileName)) != "jpeg":
                    writeError(processedURL, filePath, fileName)
            # File passed all checks.
            else:
                filesDownloaded += 1
                print("Downloaded file #" + str(filesDownloaded) + ". Line:", str(currentLine), "URL:", processedURL)
        except Exception as errorException:
            # General error catching from urllib.request
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
        print("File already exists. Line: " + str(currentLine) + " URL: " + processedURL)
    time.sleep(delayInputValue)

print("Downloaded " + str(filesDownloaded) + " files in " + str(round(time.time() - scriptStartTime, 2)) + " seconds.")
