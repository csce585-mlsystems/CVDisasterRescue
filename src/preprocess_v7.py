import numpy as np
import numpy.random
import tensorflow as tf
import os
import librosa
from tqdm import tqdm

HEIGHT = 256
WIDTH = 256
BATCH_SIZE = 32

def decode_audio(audio_binary):
    y, sr = librosa.load(audio_binary, sr=16000)
    return tf.squeeze(audio, axis=-1)

def get_waveform(filename):
    try:
        waveform, sr = librosa.load(filename, sr=16000)
        return waveform
    except:
        return []

def get_waveform_and_label(filename):
    label = get_label(filename)
    waveform = get_waveform(filename)
    return waveform, label

def get_spectrogram_image(waveform):
    waveform = tf.cast(waveform, tf.float32)
    spectrogram = tf.signal.stft(waveform, frame_length=2048, frame_step=512, fft_length=2048) #two following lines taken from tutorial
    spectrogram = tf.abs(spectrogram)
    spectrogram = tf.expand_dims(spectrogram, axis=-1)
    spectrogram = tf.image.resize(spectrogram, [HEIGHT, WIDTH])
    spectrogram = tf.image.grayscale_to_rgb(spectrogram)
    spectrogram = tf.image.per_image_standardization(spectrogram)
    return spectrogram

def preprocess(filename):
    audio, sr = librosa.load(filename, sr=16000)
    audio = librosa.util.fix_length(audio, size=80000)
    #frequencies, times, spectrogram = signal.spectrogram(audio, sr)
    spectrogram = get_spectrogram_image(audio)
    return spectrogram