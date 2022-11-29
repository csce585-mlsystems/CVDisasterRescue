import tensorflow as tf
import numpy as np
import pyaudio, wave, timeit
from preprocess_v3 import preprocess
import matplotlib.pyplot as plt

def get_pseye_mic_index():
    for i in range(0, p.get_device_count()):
        if p.get_device_info_by_index(i)["name"] == 'USB Camera-B4.09.24.1':
            print(p.get_device_info_by_index(i))
            return i

#instantiate pyaudio object
p = pyaudio.PyAudio()

# set parameters for PyAudio stream
chunk = 1024
FORMAT = pyaudio.paInt16
channels = 1
# channels = 4
sample_rate = 16000

stream = p.open(format=FORMAT,
channels=channels,
rate=sample_rate,
input=True,
frames_per_buffer=chunk
# ,input_device_index = get_pseye_mic_index() # index may vary from device to device, this quickly determines which one it is for easy connection
)

# make inference from .wav file
def sound_inference(filename, logging = False):
    spectrogram = preprocess(filename)

    sound_model = tf.keras.models.load_model(r"sound_model3.h5")
    prediction = sound_model(tf.expand_dims(spectrogram, axis=0))

    if logging:
        if prediction > 0.5:
            print(f"Human Sound! With prediction value: {prediction}")
        else:
            print(f"Nonhuman Sound! With prediction value: {prediction}")

# measure time of 1000 inferences on non-human sound
audio_inference_times = timeit.repeat(
    lambda: sound_inference('left_tap.wav'),
    number = 1,
    repeat = 1000
)
mean_ait = np.mean(audio_inference_times)
ait_stddev = np.std(audio_inference_times)

print(f'Audio inference time: {mean_ait} ± {ait_stddev} seconds')

# Audio inference time: 0.198904177344637 ± 0.021352759491556413 seconds over 1000 trials