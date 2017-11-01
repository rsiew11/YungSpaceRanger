#!/bin/bash
#the first arg is number of mics connected


echo $1

if [ "$1" = "1" ]
then
    arecord --device=hw:1,0 --format S16_LE --duration 1 --rate 44100 -c1 /noises/noise0.wav
elif [ "$1" = "2" ]
then
    arecord --device=hw:1,0 --format S16_LE --duration 1 --rate 44100 -c1 /noises/noise0.wav
    arecord --device=hw:1,1 --format S16_LE --duration 1 --rate 44100 -c1 /noises/noise1.wav
elif [ "$1" = "3" ]
then
    arecord --device=hw:1,0 --format S16_LE --duration 1 --rate 44100 -c1 /noises/noise0.wav
    arecord --device=hw:1,1 --format S16_LE --duration 1 --rate 44100 -c1 /noises/noise1.wav
    arecord --device=hw:1,2 --format S16_LE --duration 1 --rate 44100 -c1 /noises/noise2.wav
elif [ "$1" = "4" ]
then
    arecord --device=hw:1,0 --format S16_LE --duration 1 --rate 44100 -c1 /noises/noise0.wav
    arecord --device=hw:1,1 --format S16_LE --duration 1 --rate 44100 -c1 /noises/noise1.wav
    arecord --device=hw:1,2 --format S16_LE --duration 1 --rate 44100 -c1 /noises/noise2.wav
    arecord --device=hw:1,3 --format S16_LE --duration 1 --rate 44100 -c1 /noises/noise3.wav
else
    echo "$1 has to be b/t 1 and 4"
fi


