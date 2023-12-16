import cv2
from ultralytics import YOLO

# Treshold
conf_threshold = 0.2

# Class names for mapping class IDs to labels
class_names = {
    0: "person",
    1: "bicycle",
    2: "car",
    3: "motorbike",
    5: "bus",
    7: "truck"
}

# Frame
video_cap = cv2.VideoCapture("night2.jpg")

ret, frame = video_cap.read()

def get_results(model):
    
    results = model(frame)
    
    detections = []

    # loop over the results
    for result in results:
        # loop over the detections
        for data in result.boxes.data.tolist():
            x1, y1, x2, y2, confidence, class_id = data
            x = int(x1)
            y = int(y1)
            w = int(x2) - int(x1)
            h = int(y2) - int(y1)
            class_id = int(class_id)
            detections.append({'box': [x, y, x + w, y + h], 'class': class_id, 'confidence': confidence})
    return detections

def calculate_iou(boxA, boxB):
    # Calculate IoU between two bounding boxes
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)

    boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
    boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)

    iou = interArea / float(boxAArea + boxBArea - interArea)
    return iou

def calculate_precision(detections1, detections2, iou_threshold=0.5):
    true_positives = 0
    false_positives = 0

    matched_indices = set()  # Track matched detections to avoid multiple matches

    # Loop through detections from model1 and find matches in model2
    for i, detection1 in enumerate(detections1):
        for j, detection2 in enumerate(detections2):
            if j in matched_indices:
                continue  # Skip detections already matched

            iou = calculate_iou(detection1['box'], detection2['box'])
            if iou >= iou_threshold and detection1['class'] == detection2['class']:
                true_positives += 1
                matched_indices.add(j)  # Mark detection from model2 as matched
                break

    false_positives = len(detections2) - len(matched_indices)
    precision = true_positives / max((true_positives + false_positives), 1)
    return precision


def main():
    model3 = YOLO("yolov3-tinyu.pt")
    model8 = YOLO("yolov8s.pt")
    results3 = get_results(model3)
    results8 = get_results(model8)
    precision = calculate_precision(results3, results8)
    print(f"Precision: {precision:.4f}")

if __name__ == "__main__":
    main()
