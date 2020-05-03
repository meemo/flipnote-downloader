import shutil
import os.path

# Get current file directory
workingDirectory = os.getcwd() + "/"

# Make lists
comboListDeduped = []
urlList = []
jpgList = []
kwzList = []

# Create log text file
logFile = open("log.txt", "w")

# Get a list of the URLs that will be worked on
inputFile = open("cdx.txt")
for i in inputFile:
    urlList.append("http://web.archive.org/web/" + str(str(i[84:])[:105]).replace(' ', '/'))
urlList = list(set(urlList))


# Sort by file type
for i in urlList:
    if ".jpg" in i:
        jpgList.append(i)
    elif ".kwz" in i:
        kwzList.append(i)


for file in list(set(kwzList + jpgList)):
    # Extract the file name, character 101 to 128
    fileName = str(file[100:])[:-4]
    # Extract the directory name, which is from the characters 84 to 99 of the string
    userID = str(file[83:])[:-33]

    userIDDirectory = workingDirectory + "/kwz/" + userID + "/"
    fileNamePathStart = workingDirectory + "/input/" + fileName
    fileNamePathFinal = userIDDirectory + "/" + fileName

    # Make a directory based on the "/xxxxxxxxxxxxxxxx/blah.kwz/"
    #                                        ^ that part (user ID)
    # Then move any file to that folder that is listed in the initial list

    # Create the path of the uer ID to be made if it doesn't exist
    if os.path.exists(userIDDirectory) is False:
        os.mkdir(userIDDirectory)

    shutil.move(fileNamePathStart + ".jpg", fileNamePathFinal + ".jpg")
    shutil.move(fileNamePathStart + ".kwz", fileNamePathFinal + ".kwz")
