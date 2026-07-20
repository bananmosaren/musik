#!/bin/bash

ffmpeg -i "$1/cover.jpg" -i static/media/reflection-template.png -filter_complex "[0:v]vflip[flipped];[flipped][1:v]alphamerge" "$1/reflection.png"
