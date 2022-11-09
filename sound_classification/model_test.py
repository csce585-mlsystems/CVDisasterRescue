import acoular
import pyaudio

# first, let's see how many microphones we have available since we want at least 2
p = pyaudio.PyAudio()
try:
    print(p.get_default_input_device_info())
except:
    print("No mics availiable")
