import os
from human_detect import human_voice_detect
#from human_detect_2 import human_voice_detect
import sys

if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print('COMMAND FORMAT: python run_detector.py output.txt')
    
    output_file = str(sys.argv[1])
    f = open(output_file, 'w+')
    
    directory = '/Users/albinakwak/Documents/YungSpaceRanger/VAD-python/InDomain/YesVoice/'
    
    count = 0
    total = 0
    result = ''
    for file in os.listdir(directory):
        if ".wav" not in file:
            continue
        print(os.path.join(directory, file))
        result = str(human_voice_detect(os.path.join(directory,file)))
        f.write(file + ": " + result + '\n')
        #f.write(file + ": " + str(human_voice_detect(os.path.join(directory,file))) + '\n')
        
        if (str(result) == '1'):
            count += 1
        total += 1


    f.close()
    os.system('mv ' + str(sys.argv[1]) + ' ' + directory + 'output')
    print ('Accuracy: ' + str(float(count)/float(total)))
