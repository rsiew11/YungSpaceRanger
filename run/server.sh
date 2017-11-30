#!/bin/sh

# This file runs the server file transfer to listen for an incoming file
# It unzips the resulting packet and runs the data and classifier
# on those files
# If the output is 1, then it writes the GPS coordinates found to a textfile
# called GPS coordinates. The web application reads from the textfile to display
# potential humans

while [ 1 ]
do
    ######################### PACKET TRANSFER ###############################
    # Run the server file transfer to listen for an incoming file
    python ../hardware/serverFileTransfer.py &
    sleep 5

    ################## VAD CLASSIFIER ON WAVE FILE  #########################
    # The packet is located within 'packet/'
    human_detected=$(python ../VAD-python/human_detect.py ../hardware/packet/wave_file.wav ../hardware/packet/thermalData.txt)
    echo "HUMAN DETECTED"$human_detected

    # Display the GPS coordinates of the human voice found
    if [ $human_detected ]
    then
        gps_coordinates=$(python parse_gps.py ../hardware/packet/gpsLocation.txt)
        echo $gps_coordinates
    fi
    sleep 15
done

