import cv2
import time
from ultralytics import YOLO
from deep_sort.deep_sort.tracker import Tracker
from deep_sort.deep_sort import nn_matching
from deep_sort.deep_sort.detection import Detection
from deep_sort.tools import generate_detections as gdet

# Load the YOLO model
model = YOLO("yolov8s.pt")

# Initialize the deep sort tracker
model_filename = "config/mars-small128.pb"
encoder = gdet.create_box_encoder(model_filename, batch_size=1)
metric = nn_matching.NearestNeighborDistanceMetric("cosine", matching_threshold=0.5)
tracker = Tracker(metric)

# Open the video file
video_cap = cv2.VideoCapture("1.mp4")

frame_count = 0
start_time = time.time()

while True:
    ret, frame = video_cap.read()

    if not ret:
        print("End of the video file...")
        break

    # Run YOLO model on the frame
    results = model(frame)

    # Initialize lists to store detections
    bboxes = []
    confidences = []
    class_ids = []

    # Extract detections
    for result in results:
        for data in result.boxes.data.tolist():
            x1, y1, x2, y2, confidence, class_id = data
            if confidence > 0.5:  # Adjust confidence threshold as needed
                bboxes.append([x1, y1, x2 - x1, y2 - y1])
                confidences.append(confidence)
                class_ids.append(class_id)

    # Convert the detections to deep sort format
    features = encoder(frame, bboxes)
    detections = [Detection(bbox, confidence, class_id, feature) for bbox, confidence, class_id, feature in
                  zip(bboxes, confidences, class_ids, features)]

    # Update the tracker with detections
    tracker.predict()
    tracker.update(detections)

    # Count the tracked vehicles
    counter = 0
    for track in tracker.tracks:
        if track.is_confirmed() and not track.time_since_update > 1:
            counter += 1

    # Display the count of vehicles and frame rate on the frame
    cv2.putText(frame, f"Vehicles: {counter}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Display the frame with tracked objects
    for track in tracker.tracks:
        if track.is_confirmed() and not track.time_since_update > 1:
            bbox = track.to_tlbr()
            cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), (0, 255, 0), 2)

    frame_count += 1
    cv2.imshow("Tracked Objects", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

end_time = time.time()
elapsed_time = end_time - start_time
fps = frame_count / elapsed_time
print(f"Average FPS: {fps}")

video_cap.release()
cv2.destroyAllWindows()
