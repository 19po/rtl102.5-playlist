# rtl102.5-playlist
RTL 102.5 (private Italian radio station) on-the-air radio stream information parser for VLC.
Radio's website: www.rtl.it, and Wikipedia entry: https://en.wikipedia.org/wiki/RTL_102.5.

## How to use (v. 2)
Create application launcher (like here: https://help.ubuntu.com/community/UnityLaunchersAndDesktopFiles):

- Open gedit and paste as below.

    ```
    #!/usr/bin/env xdg-open

	[Desktop Entry]
	Version=1.0
	Name=RTL 102.5 Player
	Comment=Player for Italian radio station RTL 102.5
	Exec=/<your-absolute-path>/rtl102.5-playlist/Main.py
	Icon=/<your-absolute-path>/rtl102.5-playlist/images/icon.png
	Terminal=false
	Type=Application
    ```

- Save as: 
	`RTL 102.5 Player.desktop`
- validate desktop file:
	`desktop-file-validate <your-path>/rtl102.5-playlist/RTL\ 102.5\ Player.desktop`
- install desktop file in `/usr/share/applications/` location:
	`sudo desktop-file-install <your-path>/rtl102.5-playlist/RTL\ 102.5\ Player.desktop`
- Make files executable:
	`sudo chmod +x <your-path>/rtl102.5-playlist/Main.py`
	`sudo chmod +x /usr/share/applications/RTL\ 102.5\ Player.desktop`

Screenshot:

![screen 1](images/screen1.png)

![screen 2](images/screen2.png)

Application is under Python 2.7 and Qt4.
Make sure you have installed sni-qt and VLC.

## How to use (v. 1)
* Run stream `http://shoutcast.rtl.it:3010/stream/1/` using VLC.
* Open terminal and run `python rtl1025-playlist.py`.
* Example output:
```
$ python rtl1025-playlist.py 
song_cover     : http://is4.mzstatic.com/image/thumb/Music6/v4/6f/77/c4/6f77c47b-6aea-51cf-d855-839ba257b462/source/600x600bb.jpg
speakers       : Amadeus, Conte Galè, Paolo Cavallone
artist_name    : Luca Carboni
song_title     : Bologna è una regola
program_image  : http://img.rtl.it/RTLFM/speakers/400x400/amadeus-dbgwl.jpg
program_title  : Miseria e nobiltà
```
* Parsable JSON file `rtl1025-playlist.json` with the contents as above will be created.
