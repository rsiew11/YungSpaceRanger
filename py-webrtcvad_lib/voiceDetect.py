import collections
import contextlib
import sys
import wave
import webrtcvad
import argparse

def read_wave(path):
    with contextlib.closing(wave.open(path, 'rb')) as wf:
        num_channels = wf.getnchannels()
        assert num_channels == 1
        sample_width = wf.getsampwidth()
        assert sample_width == 2
        sample_rate = wf.getframerate()
        assert sample_rate in (8000, 16000, 32000)
        pcm_data = wf.readframes(wf.getnframes())
        return pcm_data, sample_rate

class Frame(object):
    def __init__(self, bytes, timestamp, duration):
        self.bytes = bytes
        self.timestamp = timestamp
        self.duration = duration

def frame_generator(frame_duration_ms, audio, sample_rate):
    n = int(sample_rate * (frame_duration_ms / 1000.0) * 2)
    offset = 0
    timestamp = 0.0
    duration = (float(n) / sample_rate) / 2.0
    while offset + n < len(audio):
        yield Frame(audio[offset:offset + n], timestamp, duration)
        timestamp += duration
        offset += n

def contains_voice(vad, sample_rate, frames):
    for frame in frames:
        if vad.is_speech(frame.bytes, sample_rate):
            return True
    return False

def main(args):
    audio, sample_rate = read_wave(args.wave_file)
    vad = webrtcvad.Vad(0)
    frames = frame_generator(30, audio, sample_rate)
    frames = list(frames)
    if (contains_voice(vad, sample_rate, frames)):
        sys.stdout.write("Voice found!\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("wave_file", help="wave file to determine if voice exists")
    args = parser.parse_args()
    main(args)

