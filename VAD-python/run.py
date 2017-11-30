from vad import VoiceActivityDetector
import sys

def main(wave_file):
    v = VoiceActivityDetector(wave_file)
    array = v.detect_speech()
    print array.tolist()
if __name__ == "__main__":
    if (len(sys.argv) != 2):
                    print('COMMAND FORMAT: python run.py input.wav output.txt')
    main(sys.argv[1])
