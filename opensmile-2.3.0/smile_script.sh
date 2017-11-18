for file in ~/Documents/YungSpaceRanger/opensmile-2.3.0/training_help/*.wav
do
    echo "Performing script on file: $file...\n"
    NAME=$(basename $file | cut -d. -f1)
    OUTPUT_DIR="/Users/albinakwak/Documents/YungSpaceRanger/opensmile-2.3.0/training_help/output"
    ./SMILExtract -C config/MFCC12_0_D_A.conf -I "$file" -csvoutput $NAME".csv"
    mv $NAME".csv" $OUTPUT_DIR
done
