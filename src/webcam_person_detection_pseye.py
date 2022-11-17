import cv2, time
from pseyepy import Camera, Display
import numpy as np 
from PIL import Image
import tensorflow as tf 
from tensorflow.python.saved_model import tag_constants
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession

import core.utils as utils
from core.yolov4 import filter_boxes

dis_cv2_window = False # sets whether or not the cv2 window appears

def model_inference(image_input, interpreter, input_details, output_details ):

    interpreter.set_tensor(input_details[0]['index'], image_input)
    interpreter.invoke()
    pred = [interpreter.get_tensor(output_details[i]['index']) for i in range(len(output_details))]

    boxes, pred_conf = filter_boxes(pred[0], pred[1], score_threshold=0.25, input_shape=tf.constant([416, 416]))

    return boxes, pred_conf 

def main(buffer):
    config = ConfigProto()
    config.gpu_options.allow_growth = True    
    session = InteractiveSession(config=config)
    # information taken from src/core/config.py
    STRIDES = [16, 32]
    ANCHORS = [23,27, 37,58, 81,82, 81,82, 135,169, 344,319]
    NUM_CLASS = 1
    XYSCALE = [1.05, 1.05]
    input_size = 416

    """ init. Webcam object 
    """
    c = Camera()
    # 640 x 480 by default

    """ Setup model 
    """
    interpreter = tf.lite.Interpreter(model_path='./checkpoints/yolov4-tiny-416.tflite')
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()


    """ Video frame input 
    """
    frame_id = 0
    count = 0

    while True:
        frame, timestamps = c.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame)

        frame_size = frame.shape[:2]
        image_data = cv2.resize(frame, (input_size, input_size))
        image_data = image_data / 255.
        image_data = image_data[np.newaxis, ...].astype(np.float32)
        prev_time = time.time()        

        """ Inference 
        """
        boxes, pred_conf = model_inference(image_data, interpreter, input_details, output_details)

        if not pred_conf.numpy().size == 0:
            buffer[count % len(buffer)] = int(time.time())
            count += 1
        # print(f'Buffer: {buffer}')

        """ Post Processing 
        """
        boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
            boxes=tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
            scores=tf.reshape(
                pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
            max_output_size_per_class=50,
            max_total_size=50,
            iou_threshold=0.45,
            score_threshold=0.45
            )        

        pred_bbox = [boxes.numpy(), scores.numpy(), classes.numpy(), valid_detections.numpy()]
        image = utils.draw_bbox(frame, pred_bbox)
        curr_time = time.time()
        exec_time = curr_time - prev_time
        result = np.asarray(image)
        info = "time: %.2f ms" %(1000*exec_time)
        
        # calculate frames per second of running detections
        fps = 1.0 / (time.time() - prev_time)
        # print("FPS: %.2f" % fps)

        result = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        cv2.imshow("CVDisasterRescue Person Detection", result)
        if cv2.waitKey(1) & 0xFF == ord('q'): break

    c.end()

    # if __name__ == '__main__':
    #     main()
