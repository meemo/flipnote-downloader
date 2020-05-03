import os
import os.path
from os import path
import urllib.request

# archive.org source URL
sourceURL = "https://web.archive.org/cdx/search/cdx?matchType=prefix&url=jkz-dsidata.s3.amazonaws.com/kwz/"

# Get current file directory
workingDirectory = os.getcwd()

# Create folder for kwz files if it doesn't exist
if path.exists(workingDirectory + '/kwz') is False:
    basePath = "/kwz"
    os.mkdir(basePath)

# CDX File Detection
isCDXFilePresent = False
if os.path.exists(workingDirectory + "cdx.txt") is False:
    print("CDX text file not detected.")
    isCDXFilePresent = False
else:
    inputFile = open(workingDirectory + 'cdx.txt')
    isCDXFilePresent = True


# Lists for processing
urlList = []
jpgList = []
kwzList = []
comboListDeduped = []


def getCDXFile():
    print("Getting CDX text file")
    urllib.request.urlretrieve(sourceURL, workingDirectory + "cdx.txt")


def processLists():
    # Put all files in the correct format for the URL that can be used to download
    for i in inputFile:
        tempString = "http://web.archive.org/web/" + str(str(i[84:])[:105]).replace(' ', '/')
        urlList.append(tempString)
    # Sort by file type
    for i in urlList:
        if ".jpg" in i:
            jpgList.append(i)
        elif ".kwz" in i:
            kwzList.append(i)
    for entry in list(set(kwzList + jpgList)):
        comboListDeduped.append(entry)


def outputLists():
    processLists()
    outputFileKWZ = open('kwz.txt', "w")
    outputFileJPG = open('jpg.txt', "w")
    # Output files to their respective text files
    for i in jpgList:
        outputFileJPG.write(i + "\n")

    for i in kwzList:
        outputFileKWZ.write(i + "\n")


def makeDirectories():
    # Make a directory based on the "/xxxxxxxxxxxxxxxx/blah.kwz/"
    #                                        ^ that part (user ID)
    # Then move any file from that containing
    # Check if there is a /kwz/ folder at the working directory yet and if not, make it
    for file in comboListDeduped:
        # Finding the file names and user ID to be made in to a directory from the URL string.
        # Extract the file name, character 101 to 128
        fileName = str(file[100:])[:-4]
        # Extract the directory name, which is from the characters 84 to 99 of the string
        userID = str(file[83:])[:-33]
        # Create the path to be made
        userIDDirectory = "/kwz/" + userID
        fileNamePath = "/kwz/" + userID + "/" + fileName
        os.mkdir(userIDDirectory)
        os.replace(fileNamePath + ".jpg", userIDDirectory + ".jpg")
        os.replace(fileNamePath + ".kwz", userIDDirectory + ".kwz")


def downloadLists():
    print("downloading")
    processLists()
    downloadingList = []
    preDownloadedList = []
    if os.path.exists(workingDirectory + "flipnotes_downloaded.txt") is True:
        preDownloadedFiles = open("flipnotes_downloaded", "w")
        for url in preDownloadedFiles:
            preDownloadedList.append(url)
        downloadingList = list(set(comboListDeduped) - set(preDownloadedList))
    preDownloadedFiles = open("flipnotes_downloaded", "w")
    for url in downloadingList:
        userID = str(url[83:])[:-33]
        print("Downloading: " + url)
        urllib.request.urlretrieve(url, workingDirectory + "kwz/" + userID + "/")
        preDownloadedFiles.write(url + "\n")
        print("Download Complete.")


hasUserChosen = False

while hasUserChosen is False:
    print("Please choose an option:")
    print("[1] Get cdx.txt file.")
    print("[2] Download all files")
    print("[3] Sort existing files in directory of script")
    print("[4] Create URL text files for KWZ and JPG files")
    print("[5] ")
    userInput = input("Option: ")
    if userInput is "1":
        print("Option 1 chosen.")
        getCDXFile()
        hasUserChosen = True
    elif userInput is "2":
        print("Option 2 chosen.")
        hasUserChosen = True
    elif userInput is "3":
        print("Option 3 chosen.")
        hasUserChosen = True
    elif userInput is "4":
        print("Option 4 chosen.")
        hasUserChosen = True
    elif userInput is "5":
        print("Option 5 chosen.")
        hasUserChosen = True
    else:
        print("Please enter a valid option")
