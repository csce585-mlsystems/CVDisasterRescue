import numpy as np
from pathlib import Path
from yolov3.configs import *
from yolov3.utils import Load_Yolo_model, detect_image, detect_realtime, detect_video_realtime_mp, detect_video
from yolov3.evaluate_mAP import get_mAP
from yolov3.dataset import Dataset

import cv2, os, random

dataset_types = ['train', 'test', 'validation']

test_image_path = 'data/Dataset/train/Human_hand/7017da3aa12bbfe2.jpg'

model = Load_Yolo_model()

# detect_image(model, test_image_path, '', input_size=YOLO_INPUT_SIZE, show=True, CLASSES=TRAIN_CLASSES, rectangle_colors=(255,0,0))

detect_realtime(model, '', input_size=YOLO_INPUT_SIZE, show=True, CLASSES=TRAIN_CLASSES, rectangle_colors=(255, 0, 0))
