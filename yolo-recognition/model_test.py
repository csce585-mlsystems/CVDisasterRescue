import numpy as np
from pathlib import Path
from PIL import Image
import tensorflow as tf
from tensorflow import keras
from yolov3.configs import *
import matplotlib.pyplot as plt


MODEL_PATH = 'model/yolov3_human_detection_Tiny'
TRAIN_CLASS_LIST = ['Human_head', 'Human_leg', 'Human_hand', 'Human_foot', 'Human_body', 'Human_arm']

model = tf.saved_model.load(MODEL_PATH)

print (model)

def load_image_to_np_array(file):
    return np.array(Image.open(file))


for i in range(0, 5): # number of training classes
    current_image_directory = 'data/Dataset/test/' + TRAIN_CLASS_LIST[i]
    for image in Path(current_image_directory).glob('*.jpg'):

        # print('Processing inference upon {}'.format(image))
        np_image = tf.constant(load_image_to_np_array(image))
        
        print(np_image)
        # input_tensor = tf.convert_to_tensor(np_image)
        # input_tensor = input_tensor[tf.newaxis, ...]
        # print(input_tensor)



        # detections = model(inputs=input_tensor)
        # print(detections)

# model = tf.saved_model.load(MODEL_PATH)

