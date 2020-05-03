import os.path
import urllib3
import html2text

# Get current file directory
workingDirectory = os.getcwd()

# URL for cdx.txt file
sourceURL = "https://web.archive.org/cdx/search/cdx?matchType=prefix&url=jkz-dsidata.s3.amazonaws.com/kwz/"

# Check if cdx.txt exists
if os.path.exists(workingDirectory + "\cdx.txt") is False:
    print("Downloading cdx.txt")
    page = urllib3.open(sourceURL)
    html_content = page.read()
    rendered_content = html2text.html2text(html_content)
    outputCDXFile = open("cdx.txt", "w")
    outputCDXFile.write(rendered_content)
    outputCDXFile.close()
else:
    # the valid cdx.txt file is 1283000268 bytes, making sure that the case with the existing file.
    if os.path.getsize(workingDirectory + "\cdx.txt") is "123000268":
        print("cdx.txt already exists!")
    else:
        print("cdx.txt is not the correct size!")

