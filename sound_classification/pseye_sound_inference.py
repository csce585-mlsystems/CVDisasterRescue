import tensorflow as tf
import numpy as np
import pyaudio, wave, os
from playsound import playsound
from preprocess import preprocess
import matplotlib.pyplot as plt

p = pyaudio.PyAudio()

def get_pseye_mic_index():
    for i in range(0, p.get_device_count()):
        if p.get_device_info_by_index(i)["name"] == 'USB Camera-B4.09.24.1':
            print(p.get_device_info_by_index(i))
            return i

#settings for recording, need to match settings that model was trained on
chunk = 1024
FORMAT = pyaudio.paInt16
channels = 4
sample_rate = 16000
record_seconds = 5

stream = p.open(
    format = FORMAT,
    channels = channels,
    rate = sample_rate,
    input=True,
    frames_per_buffer=chunk,
    input_device_index = get_pseye_mic_index() # index may vary from device to device, this quickly determines which one it is for easy connection
)

print("Recording audio...")

count = 0
while True:
    frames = []
    for i in range(int(sample_rate/chunk * record_seconds)):
        data = stream.read(chunk, exception_on_overflow=False)
        #stream.write(data)
        frames.append(data)

    print("Finished recording")

    filename = f'test{count}.wav'

    wf = wave.open(filename, "wb")
    # set the channels
    wf.setnchannels(channels)
    # set the sample format
    wf.setsampwidth(p.get_sample_size(FORMAT))
    # set the sample rate
    wf.setframerate(sample_rate)
    # write the frames as bytes
    wf.writeframes(b"".join(frames))
    # close the file
    wf.close()

    #combined = "".join([str(item) for item in frames])
    #print(combined)
    #decoded = np.fromstring(combined, float)
    #print(decoded)
    spectrogram = preprocess(filename)
    # sound_model = tf.keras.models.load_model(r"C:\Users\Scrap\Downloads\sound_model3.h5")
    sound_model = tf.keras.models.load_model(r"sound_model3.h5")
    #Tune using inter_op_parallelism_threads for best performance.
    prediction = sound_model(tf.expand_dims(spectrogram, axis=0)
)

    if prediction > 0.5:
        print(f"Human Sound! With prediction value: {prediction}")
    else:
        print(f"Nonhuman Sound! With prediction value: {prediction}")

    count += 1
    os.remove(filename)
