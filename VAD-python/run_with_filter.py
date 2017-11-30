#run.py 
#which is called in classify.sh

from vad import VoiceActivityDetector
import sys
import wave
import numpy as np

def main(wave_file, txt_output):
	
	wr = wave.open(wave_file, 'r')
	par = list(wr.getparams())
	par[3] = 0
	
	filtered_wav = wave_file[:-4]
	filtered_wav = filtered_wav+"_fltrd.wav"

	ww = wave.open(filtered_wav, 'w')
	ww.setparams(tuple(par))

	lowpass = 300
	highpass = 3400

	sz = wr.getframerate()
	c = int(wr.getnframes()/sz)
	for num in range(c):
		print('Processing {}/{} s'.format(num+1, c))
		da = np.fromstring(wr.readframes(sz), dtype=np.int16)
		left, right = da[0::2], da[1::2] # left and right channel
		lf, rf = np.fft.rfft(left), np.fft.rfft(right)
		lf[:lowpass], rf[:lowpass] = 0, 0 # low pass filter
		lf[55:66], rf[55:66] = 0, 0 # line noise
		lf[highpass:], rf[highpass:] = 0,0 # high pass filter
		nl, nr = np.fft.irfft(lf), np.fft.irfft(rf)
		ns = np.column_stack((nl,nr)).ravel().astype(np.int16)
		ww.writeframes(ns.tostring())
	wr.close()
	ww.close()

	v = VoiceActivityDetector(filtered_wav)
	with open(txt_output, "w") as open_file:
		array = v.detect_speech()
		open_file.write(str(array))
	open_file.close()

if __name__ == "__main__":
	if (len(sys.argv) != 3):
		print('COMMAND FORMAT: python run_with_filter.py input.wav output.txt')
	main(sys.argv[1], sys.argv[2])
