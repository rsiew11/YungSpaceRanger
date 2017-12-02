import os
import human_detect

if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print('COMMAND FORMAT: python run_detector.py output.txt')
    
    output_file = str(sys.argv[1])
    f = open(output_file, 'w+')
    
    for file in os.listdir('/Users/albinakwak/Documents/YungSpaceRanger/VAD-python/InDomain/Yesvoice'):
        #f.write(file + ": " + human_detect(file) + '\n')
    
    f.close()
