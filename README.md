# Usage
`downloader.py [delay in seconds (optional, defaults to 0)]`

A pre downloaded version can be found here: https://archive.org/details/flipnote-hatena-archive

Just run downloader.py in any directory, and let it run for roughly the week it will take to run.
To modify the delay between downloads of files, edit line 7 of downloader.py
**Warning: archive.org will most likely rate limit or even ban your IP from this without using proper delays and/or using a VPN. It is recommended to run this script in bursts over a long period of time, since the script will continue where you last finished downloading. The script will take about a month to run nonstop.**
# Origin
Project was inspired by https://github.com/Flipnote-Collective/flipnote-fetcher
That project lacks a bulk downloading function, so I made one myself in this script.
# cdx.txt explanation
cdx.txt is derived from the output of archive.org's cdx tool by going to the following URL:


    http://web.archive.org/cdx/search/cdx?matchType=prefix&url=jkz-dsidata.s3.amazonaws.com/kwz/

And saving the page as a text file.
