import tensorflow as tf
import numpy as np
import pyaudio
import wave
from playsound import playsound
from preprocess import preprocess
import matplotlib.pyplot as plt


#settings for recording, need to match settings that model was trained on
chunk = 1024
FORMAT = pyaudio.paInt16
channels = 1
sample_rate = 16000
record_seconds = 5

count = 0

#instantiate pyaudio object
p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
channels=channels,
rate=sample_rate,
input=True,
output=True,
frames_per_buffer=chunk)

print("Recording audio...")

while True:
    frames = []
    for i in range(int(sample_rate/chunk * record_seconds)):
        data = stream.read(chunk, exception_on_overflow=False)
        #stream.write(data)
        frames.append(data)
        print(data)

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
