import tensorflow as tf
from pathlib import Path
import numpy as np
from yolov3.configs import *
from yolov3.utils import Load_Yolo_model, detect_image, detect_realtime, detect_video_realtime_mp, detect_video, image_preprocess, postprocess_boxes, nms, bboxes_iou
import cv2, os

model = Load_Yolo_model() # loads our Yolo model (Keras functional model) from checkpoints folder saved in TFRecord format currently
root_test_data_dir = 'data/Dataset/test'
test_subsets = ['Human_leg', 'Human_head', 'Human_hand', 'Human_foot', 'Human_body', 'Human_arm']

def nms_iou(bboxes, iou_threshold, sigma=0.3, method='nms'):
    classes_in_img = list(set(bboxes[:, 5]))
    best_bboxes = []
    iou_scores = []

    for cls in classes_in_img:
        cls_mask = (bboxes[:, 5] == cls)
        cls_bboxes = bboxes[cls_mask]
        # Process 1: Determine whether the number of bounding boxes is greater than 0 
        while len(cls_bboxes) > 0:
            # Process 2: Select the bounding box with the highest score according to socre order A
            max_ind = np.argmax(cls_bboxes[:, 4])
            best_bbox = cls_bboxes[max_ind]
            best_bboxes.append(best_bbox)
            cls_bboxes = np.concatenate([cls_bboxes[: max_ind], cls_bboxes[max_ind + 1:]])
            # Process 3: Calculate this bounding box A and
            # Remain all iou of the bounding box and remove those bounding boxes whose iou value is higher than the threshold 
            iou = bboxes_iou(best_bbox[np.newaxis, :4], cls_bboxes[:, :4])
            iou_scores.append(iou)
            weight = np.ones((len(iou),), dtype=np.float32)

            assert method in ['nms', 'soft-nms']

            if method == 'nms':
                iou_mask = iou > iou_threshold
                weight[iou_mask] = 0.0

            if method == 'soft-nms':
                weight = np.exp(-(1.0 * iou ** 2 / sigma))

            cls_bboxes[:, 4] = cls_bboxes[:, 4] * weight
            score_mask = cls_bboxes[:, 4] > 0.
            cls_bboxes = cls_bboxes[score_mask]

    return iou_scores, best_bboxes

test_item_count = 0
total_iou_score = 0 # images with multiple bounding boxes will have IoU scores for each one
undetectable_images = 0

for subset in test_subsets:
    for image_path in Path(os.path.join(root_test_data_dir, subset)).glob('*.jpg'):
        original_image      = cv2.imread(str(image_path))
        original_image      = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

        image_data = image_preprocess(np.copy(original_image), [YOLO_INPUT_SIZE, YOLO_INPUT_SIZE])
        image_data = image_data[np.newaxis, ...].astype(np.float32)

        predicted_bbox = model.predict(image_data)
        predicted_bbox = [tf.reshape(x, (-1, tf.shape(x)[-1])) for x in predicted_bbox]
        predicted_bbox = tf.concat(predicted_bbox, axis=0)

        bboxes = postprocess_boxes(predicted_bbox, original_image, YOLO_INPUT_SIZE, 0.2)
        iou_scores, best_bboxes = nms_iou(bboxes, 0, method='nms')
        test_item_count += 1
        for i in range(0, len(iou_scores)):
            try:
                total_iou_score += iou_scores[i]
            except:
                total_iou_score += 0
                undetectable_images += 1

print(f'Number of test images: {test_item_count}\nNumber of images that our model could not draw bounding boxes for: {undetectable_images}\nBounding box draw success rate: {(test_item_count - undetectable_images) / test_item_count}\nAverage IoU score per image: {total_iou_score[0] / test_item_count}\nAverage IoU score per successful image: {total_iou_score[0] / (test_item_count - undetectable_images)}')
