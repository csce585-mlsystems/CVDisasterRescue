import logging
logging.getLogger("tensorflow").setLevel(logging.DEBUG)

import tensorflow as tf
import numpy as np
from yolov3.utils import Load_Yolo_model

# load model from checkpoints directory as TFRecord format
yolo = Load_Yolo_model()

# save model as .h5 file
yolo.save('model/yolov3_human_detection.h5')

# Dynamic Range Quantization
# statically quantizes the weights from floating point to 8-bits of precision and dynamically quantizes the activations at inference
model = tf.keras.models.load_model('model/yolov3_human_detection.h5')
converter = tf.lite.TFLiteConverter.from_keras_model(yolo)
# converter.optimizations = [tf.lite.Optimize.DEFAULT]

# convert to TFLite model
tflite_human_detection = converter.convert()

open('model/tflite_human_detection.tflite', 'wb').write(tflite_human_detection)