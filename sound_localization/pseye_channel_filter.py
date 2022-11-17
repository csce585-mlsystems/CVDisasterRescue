import pyaudio, wave, os, librosa
import numpy as np

# Channels on the PS Eye go from 0 -> 3 (4 total channels) left to right

test_file_path = '../sound_classification/right_tap.wav'

data, sample_rate = librosa.load(test_file_path, sr=16000, mono=False)

print(f'Channel {np.argmax(np.mean(data, axis=1))} is the loudest with an amplitude of {np.mean(data, axis=1)[np.argmax(np.mean(data, axis=1))]}')