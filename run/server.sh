#!/bin/sh

# This file runs the server file transfer to listen for an incoming file
# It unzips the resulting packet and runs the data and classifier
# on those files
# If the output is 1, then it writes the GPS coordinates found to a textfile
# called GPS coordinates. The web application reads from the textfile to display
# potential humans
var=0
while [ 1 ]
do
    ######################### PACKET TRANSFER ###############################
    # Run the server file transfer to listen for an incoming file
    sudo nc -l 22 > pac.zip
    unzip -o pac.zip

    #var=$((var + 1))
    #new_file="noise"$var".wav"
    #scp packet/noise0.wav test_data/$new_file
    ################## VAD CLASSIFIER ON WAVE FILE  #########################
    # The packet is located within 'packet/'
    human_detected=$(python ../VAD-python/human_detect.py packet/noise0.wav packet/thermalData.txt)
    echo "HUMAN DETECTED ? "$human_detected

    # Display the GPS coordinates of the human voice found
    if [ $human_detected ]
    then
        gps_coordinates=$(python parse_gps.py ../hardware/packet/gpsLocation.txt)
        echo $gps_coordinates
    fi
done

