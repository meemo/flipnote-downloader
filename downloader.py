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
print("In that time, you may have your IP blocked from archive.org.")
print("Please set a delay value wisely! Delay is currently set to " + str(delayInputValue) + " seconds.")
time.sleep(3)

if os.path.exists(os.path.join(downloadingDirectory)) is False:
    os.mkdir(os.path.join(downloadingDirectory))
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
    processedURL = str("http://web.archive.org/web/" + str(str(i[84:])[:105]).replace(" ", "if_/"))
    # File name: characters 101 to 128. Author ID: characters 84 to 99
    fileName = processedURL[103:]
    authorID = str(processedURL[86:])[:-33]
    filePath = os.path.join(downloadingDirectory, authorID)
    if os.path.exists(filePath) is False:
        os.mkdir(filePath)
    if os.path.isfile(os.path.join(filePath, fileName)) is False:
        try:
            urlOpener = urllib.request.build_opener()
            urlOpener.addheaders = [('Content-type', 'application/octet-stream')]
            urllib.request.install_opener(urlOpener)
            urllib.request.urlretrieve(processedURL, os.path.join(filePath, fileName))
            if os.path.getsize(os.path.join(filePath, fileName)) == 0:
                # Check for 0 byte files
                print("0 Byte file detected!")
                open("error_files_deleted.txt", "a", newline="\n").write(processedURL + "\n")
                os.remove(os.path.join(filePath, fileName))
                print("Deleted invalid file.")
            elif ".kwz" in fileName:
                # kwz files always start with "KFH" when decoded to ansi.
                if str(open(os.path.join(filePath, fileName), "rb").read().decode("ansi")).startswith("KFH") is False:
                    open("error_files_deleted.txt", "a", newline="\n").write(processedURL + "\n")
                    os.remove(os.path.join(filePath, fileName))
                    print("Deleted invalid file.")
            elif ".jpg" in fileName:
                # Ensure jpg files are valid using imghdr
                if imghdr.what(os.path.join(filePath, fileName)) != "jpeg":
                    open("error_files_deleted.txt", "a", newline="\n").write(processedURL + "\n")
                    os.remove(os.path.join(filePath, fileName))
                    print("Deleted invalid file.")
            else:
                # File passed all checks
                filesDownloaded += 1
                print("Downloaded file #" + str(filesDownloaded) + ", line " + str(currentLine) + ", URL: "
                      + processedURL)
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
        print("Duplicate on line: " + str(currentLine) + " URL: " + processedURL)
    time.sleep(delayInputValue)

print("Downloaded " + str(filesDownloaded) + " files in " + str(round(time.time() - scriptStartTime, 2)) + " seconds.")
