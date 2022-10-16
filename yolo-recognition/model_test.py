
from pickletools import optimize
import numpy as np
from pathlib import Path
from PIL import Image
import tensorflow as tf
from tensorflow import keras, expand_dims
from keras.models import load_model, Model
from yolov3.configs import *
from yolov3.yolov4 import Create_Yolo
from yolov3.evaluate_mAP import get_mAP
from yolov3.dataset import Dataset
from matplotlib import pyplot
import cv2, os

MODEL_PATH = 'model/yolov3_human_detection_Tiny'
TRAIN_CLASS_LIST = ['Human_head', 'Human_leg', 'Human_hand', 'Human_foot', 'Human_body', 'Human_arm']
anchors = YOLO_ANCHORS
checkpoint_path = os.path.dirname('training_checkpoints')

model = Create_Yolo(input_size=416, training=False, CLASSES=TRAIN_CLASSES)
model.load_weights('model/yolov3_human_detection_Tiny.h5')

test_image_path = 'data/Dataset/test/Human_leg/0c77133742ceb85e.jpg'
# print(model.summary())

input_w, input_h = 416, 416