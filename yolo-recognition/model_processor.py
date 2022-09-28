from yolov3.configs import *
from yolov3.yolov4 import *

yolo = Create_Yolo(input_size=YOLO_INPUT_SIZE, CLASSES=TRAIN_CLASSES)
checkpoint = f"./training_checkpoints/{TRAIN_MODEL_NAME}_Tiny"
save_dest = f'./model/{TRAIN_MODEL_NAME}_Tiny'
yolo.load_weights(checkpoint)

print(yolo)
yolo.save(save_dest)
yolo.save_weights(save_dest + '.h5')
