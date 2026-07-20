#!/bin/bash

# Downloads all tracks to "tracks" folder and names them after order
mkdir $1/tracks
yt-dlp -x --audio-format mp3 -o "%(autonumber)s" --paths "$1/tracks" "$2"

# Downloads album cover as cover.jpg
yt-dlp --skip-download --write-thumbnail --convert-thumbnails jpg --playlist-items 0 -o "cover.%(ext)s" --paths "$1" "$2"

