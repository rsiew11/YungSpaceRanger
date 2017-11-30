from vad import VoiceActivityDetector
import sys
import wave
import numpy as np

human_temp_threshold = 25.0

def parse_voice_array(voice_array):
    avg_sum = 0
    voice_sum = 0
    num_elements = len(voice_array)
    for element in voice_array:
        voice_sum += int(element[1])
    if (voice_sum):
        return 1
    return 0

def perform_bandpass(wave_file):
    # Created input file with:
    # mpg123  -w 20130509talk.wav 20130509talk.mp3
    wr = wave.open(wave_file, 'r')
    par = list(wr.getparams()) # Get the parameters from the input.
    # This file is stereo, 2 bytes/sample, 44.1 kHz.
    par[3] = 0 # The number of samples will be set by writeframes.

    # Open the output file
    filtered_wave = '/Users/namritamurali/Documents/Documents - Nams MBP/CMU F17/18500/YungSpaceRanger/VAD-python/filtered_file.wav'
    ww = wave.open(filtered_wave, 'w')
    ww.setparams(tuple(par)) # Use the same parameters as the input file.

    lowpass = 300 # Remove lower frequencies.
    highpass = 3400 # Remove higher frequencies.

    sz = wr.getframerate() # Read and process 1 second at a time.
    c = int(wr.getnframes()/sz) # whole file
    for num in range(c):
        da = np.fromstring(wr.readframes(sz), dtype=np.int16)
        left, right = da[0::2], da[1::2] # left and right channel
        lf, rf = np.fft.rfft(left), np.fft.rfft(right)
        lf[:lowpass], rf[:lowpass] = 0, 0 # low pass filter
        lf[55:66], rf[55:66] = 0, 0 # line noise
        lf[highpass:], rf[highpass:] = 0,0 # high pass filter
        nl, nr = np.fft.irfft(lf), np.fft.irfft(rf)
        ns = np.column_stack((nl,nr)).ravel().astype(np.int16)
        ww.writeframes(ns.tostring())
    # Close the files.
    wr.close()
    ww.close()
    return wave_file

def human_voice_detect(wave_file):
    # band pass filter
    perform_bandpass(wave_file)
    v = VoiceActivityDetector(wave_file)
    array = v.detect_speech()
    return parse_voice_array(array.tolist())

def human_temp_detect(ir_file):
    with open(ir_file, 'r') as open_file:
        # there is only one line in this file
        line = open_file.readlines()[0]
        line = line.strip()
        line = line.strip('[')
        line = line.strip(']')
        values = line.split(',')
        for value in values:
            if (float(value) >= human_temp_threshold):
                return 1
    return 0

if __name__ == "__main__":
    if (len(sys.argv) != 3) :
        print('COMMAND FORMAT: python human_detect.py input.wav input.txt')

    wave_file = str(sys.argv[1])
    ir_file = str(sys.argv[2])

    if (human_voice_detect(wave_file) and human_temp_detect(ir_file)):
        print 1
    else:
        print 0

