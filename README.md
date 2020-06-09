# Usage
I will soon be uploading this to archive.org, so you do not need to run this script!
Just run downloader.py in any directory, and let it run for roughly the week it will take to run.
To modify the delay between downloads of files, edit line 7 of downloader.py
**Warning: archive.org will most likely rate limit or even ban your IP from this without using proper delays and/or using a VPN. It is recommended to run this script in bursts over a long period of time, since the script will continue where you last finished downloading.**
# Origin
Project was inspired by https://github.com/Flipnote-Collective/flipnote-fetcher
That project lacks a bulk downloading function, so I made one myself
# Files.zip
Files.zip contains an HTML file snapshot of the entire output of this script, created with Snap2HTML
https://www.rlvision.com/snap2html/
https://github.com/rlv-dan/Snap2HTML
# cdx.txt
cdx.txt is derived from the output of archive.org's cdx tool by going to the following URL:


    http://web.archive.org/cdx/search/cdx?matchType=prefix&url=jkz-dsidata.s3.amazonaws.com/kwz/

And saving the page as a text file. I already did this and have added together the many different versions with varying amounts of entries for easier downloading.
# TL;DR
This is a script that will download [archive.org](https://www.archive.org)'s copy of Flipnote Hatena Gallery's S3 buckets in the correct (original) folder structure.  
