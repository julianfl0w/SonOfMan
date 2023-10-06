import cv2
import numpy as np
import tensorflow as tf
from object_detection.utils import config_util
from object_detection.builders import model_builder
from object_detection.utils import visualization_utils as viz_utils
from object_detection.utils import label_map_util

# Load the pre-trained TensorFlow model
PATH_TO_CFG = "./ssd_mobilenet_v2_coco/pipeline.config"
PATH_TO_CKPT = "./ssd_mobilenet_v2_coco/checkpoint"
PATH_TO_LABELS = "./ssd_mobilenet_v2_coco/label_map.pbtxt"

# Load the pipeline configuration and build the detection model
configs = config_util.get_configs_from_pipeline_file(PATH_TO_CFG)
model_config = configs['model']
detection_model = model_builder.build(model_config=model_config, is_training=False)

# Restore the checkpoint
ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)
ckpt.restore(PATH_TO_CKPT).expect_partial()

# Load the label map
category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS)

def detect_fn(image):
    """Detect objects in the image."""
    image_np = np.array(image)
    # Convert the image to tensor format
    input_tensor = tf.convert_to_tensor([image_np])
    detections = detection_model(input_tensor)
    return detections[0]

url = 'http://localhost:5000/video_feed'
cap = cv2.VideoCapture(url)
frame_counter = 0

while True:
    ret, frame = cap.read()
    if ret:
        frame_counter += 1
        
        # Object Detection
        detections = detect_fn(frame)
        viz_utils.visualize_boxes_and_labels_on_image_array(
            frame,
            detections['detection_boxes'].numpy(),
            detections['detection_classes'].numpy().astype(np.int32),
            detections['detection_scores'].numpy(),
            category_index,
            use_normalized_coordinates=True,
            max_boxes_to_draw=200,
            min_score_thresh=.30,
            agnostic_mode=False
        )
        
        cv2.imshow('Stream', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        print("Failed to retrieve frame")
        break

cap.release()
cv2.destroyAllWindows()
