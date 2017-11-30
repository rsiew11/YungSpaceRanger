for file in ~/Documents/YungSpaceRanger/VAD-python/YesVoice/*.wav
do
    echo "Performing script on file: $file...\n"
    NAME=$(basename $file | cut -d. -f1)
	OUTPUT_DIR="/Users/albinakwak/Documents/YungSpaceRanger/VAD-python/YesVoice/output"
    python run.py "$file" $NAME".txt"
    mv $NAME".txt" $OUTPUT_DIR
done
