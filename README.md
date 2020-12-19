Xsubs TV Subtitles
============

Greek subtitles agent plugin for Plex Media Server using the Xsubs.tv site.

Download and extract the zip folder at plugins directory of Plex Media Server.
Windows: C:\Users\username\AppData\Local\Plex Media Server\Plug-ins\
## Installation

* Grab the [latest release](https://github.com/pannal/Xsubs.bundle/releases/latest)
* unpack it
* place the `Xsubs.bundle` folder inside Plug-ins folder, Windows: `C:\Users\{user}\AppData\Local\Plex Media Server\Plug-ins\`, `~/Library/Application Support/Plex Media Server/Plug-ins/`
* restart your Plex Media Server.

Additionally, you need to enable the plugin for the library:
- go to Settings -> Server -> Agents -> TV Shows.
- select the TheTVDB metadata provider on your library.
- enable Xsubs TV Subtitles
- configure username/password for http://xsubs.tv/xforum/ account, it is necessary otherwise there is a limit, 5 downloads/45 minutes for unregistered users.
- refresh your library (or individual TV shows)


## Changelog
o.3

* Rewrite from scratch.
* Add optional authentication to xsubs.tv site. 
* Remove xsubs.srt extension causing plex always transcode.
