# inspired from https://machinelearningmastery.com/how-to-perform-object-detection-with-yolov3-in-keras/

import numpy as np
from pathlib import Path
from PIL import Image
import tensorflow as tf
from tensorflow import keras, expand_dims
from keras.models import load_model, Model
from keras.layers import Conv2D, Input
from keras.utils import load_img, img_to_array
from yolov3.configs import *
from yolov3.yolov4 import Create_Yolo
import matplotlib.pyplot as plt
from yolov3.detection_utils import *

MODEL_PATH = 'model/yolov3_human_detection_Tiny'
TRAIN_CLASS_LIST = ['Human_head', 'Human_leg', 'Human_hand', 'Human_foot', 'Human_body', 'Human_arm']

model = Create_Yolo(input_size=416, training=False, CLASSES=TRAIN_CLASSES)
model.load_weights('model/yolov3_human_detection_Tiny.h5')

test_image_path = 'data/Dataset/test/Human_leg/0c77133742ceb85e.jpg'

print(model.summary())



# for i in range(0, 5): # number of training classes
#     current_image_directory = 'data/Dataset/test/' + TRAIN_CLASS_LIST[i]
#     for image in Path(current_image_directory).glob('*.jpg'):
