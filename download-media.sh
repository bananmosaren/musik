#!/bin/bash

# Downloads album cover as cover.jpg
yt-dlp --skip-download --write-thumbnail --convert-thumbnails jpg --playlist-items 0 -o "cover.%(ext)s" --paths "$1" "$2"

# Create reflection image
ffmpeg -i "$1/cover.jpg" -i static/media/reflection-template.png -filter_complex "[0:v]vflip[flipped];[flipped][1:v]alphamerge" "$1/reflection.png"

# Downloads all tracks to "tracks" folder and names them after order
mkdir $1/tracks
yt-dlp -x --audio-format mp3 -o "%(autonumber)s" --paths "$1/tracks" "$2"

