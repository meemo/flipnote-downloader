# Usage
`downloader.py [delay in seconds (optional, defaults to 0)]`

**Warning: Set a reasonable delay value to limit load on archive.org's servers and thus prevent you from being rate limited or even IP banned from archive.org. I accept no responsibilty for what is done with this script. This will take about 1 or 2 months to run with a 1 second delay through all approximately 960,000 entries (varies) and totals approximately 133.5 GB in 960,000 files.**
# Description
Flipnote Studio 3D DSi Gallery contained nearly every flipnote (excluding flipnotes from those who opted out) from the defunct Flipnote Hatena service for the original Flipnote Studio. Archive.org scraped a small portion of this via the Wayback Machine which is avaliable for any user to download. This script accesses the Wayback Machine's API and recursively downloads every file avaliable, preserving the original folder structure. The files downloaded are .kwz and .jpg, with kwz being the flipnotes and jpg being the thumbnails for each flipnote.  Documentation of the KWZ format by the Flipnote Collective can be found [here](https://github.com/Flipnote-Collective/flipnote-studio-3d-docs/wiki/kwz-format).
# Source Code
Source code can be found at https://github.com/meemo/flipnote-downloader/
