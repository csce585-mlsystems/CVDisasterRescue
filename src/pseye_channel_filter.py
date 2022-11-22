import librosa
import numpy as np

# Channels on the PS Eye go from 0 -> 3 (4 total channels) left to right

def return_average_loudest_channel(file_path):
    data, sample_rate = librosa.load(file_path, sr=16000, mono=False)
    return np.mean(data, axis=1)[np.argmax(np.mean(data, axis=1))]

def return_loudest_total_channel(file_path):
    data, sample_rate = librosa.load(file_path, sr=16000, mono=False)
    return np.argmax([np.argmax(i) for i in data])