# rtl102.5-playlist
RTL 102.5 (private Italian radio station) on-the-air playlist parser for VLC.

Radio's website: www.rtl.it, and Wikipedia entry: https://en.wikipedia.org/wiki/RTL_102.5

## How to use
* Run `stream http://shoutcast.rtl.it:3010/stream/1/` using VLC.
* Open terminal and run `python vlc_DAB_info.py`.
* Example output:
```
$ python rtl1025-playlist.py 
speakers   : Gigio D'Ambrosio, Laura Ghislandi
artist     : Lukas Graham
song       :  Years
song-cover : http://is2.mzstatic.com/image/thumb/Music6/v4/18/af/71/18af71aa-d835-1902-bc1c-6300d62aad91/source/600x600bb.jpg
prog-image : http://img.rtl.it/RTLFM/team/400x400/gigio-d-and-number-039ambrosio-laura-ghislandi-bdtex.jpg
programme  : Suite f.
```
* Parsable JSON file `rtl1025-playlist.json` with the contents as above will be created.
