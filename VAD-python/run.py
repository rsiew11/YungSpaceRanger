from vad import VoiceActivityDetector
import sys

def main(wave_file, txt_output):
		v = VoiceActivityDetector(wave_file)
		with open(txt_output, "w") as open_file:
				array = v.detect_speech()
				open_file.write(str(array))
		open_file.close()

if __name__ == "__main__":
	if (len(sys.argv) != 3):
			print('COMMAND FORMAT: python run.py input.wav output.txt')
	main(sys.argv[1], sys.argv[2])
