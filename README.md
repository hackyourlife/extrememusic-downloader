extrememusic downloader
=======================

This tool allows you to download any album or playlist from
[extrememusic](https://www.extrememusic.com). But you only get 128-192kbps mp3
files.

Usage
=====

    ./extremedownload.py 1796

This will download the album "LEGEND" (XTS016) into the folder `XTS016 - LEGEND`.

    ./extremedownload.py -p fpKK60p4U6KfApfAAfKUKpp2CyH5ZGI_7f4fU3fUK8fAA3fpfKUAUKUfAAKO6tb

This will download the playlist "TWISTED XMAS" into the folder `TWISTED XMAS`.


Album ID
========

Open https://www.extrememusic.com/ in a browser and search for the album. You
will end up with an url like https://www.extrememusic.com/albums/1796 where the
1796 is the album id that needs to be passed to the download script.

Playlist ID
===========

Same as Album ID but the url looks like this:

    https://www.extrememusic.com/playlists/fpKK60p4U6KfApfAAfKUKpp2CyH5ZGI_7f4fU3fUK8fAA3fpfKUAUKUfAAKO6tb

Attention
=========

**Respect Copyrights!**
