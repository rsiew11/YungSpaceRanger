import wave
import random
import struct

noise_output = wave.open('noise1.wav', 'w')
noise_output.setparams((2, 2, 44100, 0, 'NONE', 'not compressed'))
#                      (nchannels, sampwidth, framerate, nframes, comptype, compname),


values = []

for i in range(0, 50000):
    value = random.randint(-32767, 32767)
    packed_value = struct.pack('h', value)
    values.append(packed_value)
    values.append(packed_value)

value_str = ''.join(values)
noise_output.writeframes(value_str)

noise_output.close()

