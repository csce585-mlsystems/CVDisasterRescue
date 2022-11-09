import numpy as np
import numpy.random
import tensorflow as tf
import os
import librosa
from tqdm import tqdm
import wave
import matplotlib.pyplot as plt

data_dir = r"C:\Users\Scrap\OneDrive\Documents\Homework\CSCE585\CVDisasterRescue\sound_classification\data\model_data"

HEIGHT = 128
WIDTH = 128

def load_data(data_dir):
    classes = [x for x in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, x))]
    class_labels ={
        'human_sounds': 1,
        'nonhuman_sounds': 0}
    examples = []
    for cla in classes:
        for file in os.listdir(os.path.join(data_dir, cla)):
            examples.append([os.path.join(data_dir, cla, file), class_labels[cla]])
    return np.array(examples)

def preprocess(data, labels): #preprocessing all examples at once, typically not best practice but dataset is small
    data_dir = r"C:\Users\Scrap\OneDrive\Documents\Homework\CSCE585\CVDisasterRescue\sound_classification\data\model_data\human_sounds"
    new_X = []
    count = 0
    for row in tqdm(data):
        '''
        #samplerate, audio_data = wavfile.read(row[0])
        #resampled_audio = resample(audio_data, 16000)
        obj_read = wave.open(row[0], 'r')
        nframes = obj_read.getnframes()
        audio_data = obj_read.readframes(nframes)
        obj = wave.open(row[0], 'w')
        obj.setframerate(16000)
        obj.setnchannels(1)
        obj.setsampwidth(sample_width)
        obj.writeframesraw(resampled_audio)
        obj.close()
        obj_read.close()'''
        try:
            audio, samplerate = librosa.load(row[0], sr=16000)
            audio = librosa.util.fix_length(audio, size=52565)
            audio = tf.squeeze(audio, axis=-1)
            spectrogram = get_spectrogram(audio)
            new_X.append(spectrogram)
        except:
            np.delete(data, count, axis=0)
        count += 1
            
    '''
        if len(audio) > max_channels:
            max_channels = len(audio)
        elif len(audio) < min_channels:
            min_channels = len(audio)
    print(max_channels)
    print(min_channels)
    return np.array(new_X)'''
    return tf.data.Dataset.from_tensor_slices(new_X)

def get_spectrogram(waveform):
    waveform = tf.cast(waveform, tf.float32)
    spectrogram = tf.signal.stft(waveform, frame_length=2048, frame_step=512, fft_length=2048) #two following lines taken from tutorial
    spectrogram = tf.abs(spectrogram)
    spectrogram = tf.expand_dims(spectrogram, axis=-1)
    spectrogram = tf.image.resize(spectrogram, [HEIGHT, WIDTH])
    spectrogram = tf.image.grayscale_to_rgb(spectrogram)
    return spectrogram

    

data = load_data(data_dir)
np.random.shuffle(data)
X = data[:, :-1]
y = data[:, -1]
dataset = preprocess(X, y)
for val in X:
    print(val)
    
    break
    
