import os
#from human_detect import human_voice_detect
from human_detect_2 import human_voice_detect
import sys

if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print('COMMAND FORMAT: python run_detector.py output.txt')
    
    output_file = str(sys.argv[1])
    f = open(output_file, 'w+')
    
    directory = '/Users/albinakwak/Documents/YungSpaceRanger/VAD-python/InDomain/NoVoice/'
    for file in os.listdir(directory):
        if ".wav" not in file:
            continue
        print(os.path.join(directory, file))
        f.write(file + ": " + str(human_voice_detect(os.path.join(directory,file))) + '\n')
    
    f.close()
