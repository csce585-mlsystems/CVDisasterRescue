import core.utils as utils
utils.bbox_iou
from pathlib import Path
import os, cv2
from core.yolov4 import filter_boxes
import numpy as np
import pandas as pd
from PIL import Image
from absl import app, flags, logging  # argparse 대용인가?; (ref) https://github.com/abseil/abseil-py
from absl.flags import FLAGS
import tensorflow as tf 
from tensorflow.python.saved_model import tag_constants
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession

def model_inference(image_list):

    interpreter = tf.lite.Interpreter(model_path='checkpoints/yolov4-tiny-416.tflite')
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
#    print(input_details)
#    print(output_details)
    interpreter.set_tensor(input_details[0]['index'], image_list)
    interpreter.invoke()
    pred = [interpreter.get_tensor(output_details[i]['index']) for i in range(len(output_details))]
    boxes, pred_conf = filter_boxes(pred[0], pred[1], score_threshold=0.25, input_shape=tf.constant([416, 416]))
    return boxes, pred_conf 


def generate_boxes(image_file_path):

    final_bboxes = []

    original_image = cv2.imread(image_file_path)
    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB) # convert BGR to RGB for 'PIL'
    image_data = cv2.resize(original_image, (416, 416))
    image_data = image_data / 255.

    image_list = []

    for i in range(1):
        image_list.append(image_data)
    image_list = np.asarray(image_list).astype(np.float32)    

    boxes, pred_conf = model_inference(image_list)

    boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
        boxes=tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
        scores=tf.reshape( pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
        max_output_size_per_class=50,
        max_total_size=50,
        # iou_threshold=0.25,
        # score_threshold=0.5
        iou_threshold=0.0,
        score_threshold=0.0
    )

    pred_bbox = [boxes.numpy(), scores.numpy(), classes.numpy(), valid_detections.numpy()]

    num_classes = len(classes)
    image_h, image_w, _ = original_image.shape 

    out_boxes, out_scores, out_classes, num_boxes = pred_bbox
    for i in range(num_boxes[0]):
        if int(out_classes[0][i]) < 0 or int(out_classes[0][i]) > num_classes: continue
        
        box = out_boxes[0][i]
        ymin = int(box[0] * image_h)
        xmin = int(box[1] * image_w)
        ymax = int(box[2] * image_h)
        xmax = int(box[3] * image_w)
        final_bboxes.append([xmin, ymin, xmax, ymax])
    return final_bboxes

def iou(boxA, boxB):
	# determine the (x, y)-coordinates of the intersection rectangle
	xA = max(boxA[0], boxB[0])
	yA = max(boxA[1], boxB[1])
	xB = min(boxA[2], boxB[2])
	yB = min(boxA[3], boxB[3])
	# compute the area of intersection rectangle
	interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
	# compute the area of both the prediction and ground-truth
	# rectangles
	boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
	boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)
	# compute the intersection over union by taking the intersection
	# area and dividing it by the sum of prediction + ground-truth
	# areas - the interesection area
	iou = interArea / float(boxAArea + boxBArea - interArea)
	# return the intersection over union value
	return iou

# OID label format:
# class_name xmin, ymin, xmax, ymax

image_folder_path = 'OID/Dataset/test/Person'
label_folder_path = 'OID/Dataset/test/Person/Label'

if __name__ == '__main__':
    config = ConfigProto()
    config.gpu_options.allow_growth = True    
    session = InteractiveSession(config=config)

    test_image_count = 0
    bbox_total_count = 0
    total_iou_score = 0
    undetected_boxes = 0
    
    for label_file in Path(label_folder_path).glob('*.txt'): # traverse over each label file in directory
        image_file_path = os.path.join(image_folder_path, Path(os.path.relpath(label_file, label_folder_path)).with_suffix('.jpg')) # get corresponding image file to label
        test_image_count += 1

        experimental_bboxes = generate_boxes(image_file_path)
        bbox_total_count += len(experimental_bboxes)

        actual_bboxes = []

        df = pd.read_csv(label_file, sep=' ', skip_blank_lines=True, names=['class_name', 'xmin', 'ymin', 'xmax', 'ymax'])
        for index, row in df.iterrows():
            bbox = [row['xmin'], row['ymin'], row['xmax'], row['ymax']]
            actual_bboxes.append(bbox)

        for i in range(0, len(actual_bboxes)):
            try:
                if (iou(actual_bboxes[i], experimental_bboxes[i]) == 0.0):
                    print(f'actual_boxes: {actual_bboxes[i]}\nexperimental_boxes: {experimental_bboxes[i]}\nimage path: {image_file_path}\nlabel file path: {label_file}')

                total_iou_score += iou(actual_bboxes[i], experimental_bboxes[i])
            except:
                print('Dropped box. Not counting.')
                undetected_boxes += 1
                

    print(f'\nTotal image count: {test_image_count}\nTotal number of bounding boxes: {bbox_total_count}\nAverage IoU score per detected bounding box: {total_iou_score / (bbox_total_count - undetected_boxes)}\n')
