for file in ~/Documents/18500/opensmile-2.3.0/testing_data/*.wav
do
    echo "Performing script on file: $file...\n"
    NAME=$(basename $file | cut -d. -f1)
    OUTPUT_DIR="/afs/ece.cmu.edu/usr/yaesunk/Documents/18500/opensmile-2.3.0/testing_data/output"
    ./SMILExtract -C config/MFCC12_0_D_A.conf -I "$file" -csvoutput $NAME".csv"
    mv $NAME".csv" $OUTPUT_DIR
done
