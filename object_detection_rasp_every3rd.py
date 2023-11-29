import cv2
import time
from ultralytics import YOLO

# Load the YOLO model
model = YOLO("yolov8s.pt")

# Open the video file
video_cap = cv2.VideoCapture("1.mp4")

frame_count = 0
start_time = time.time()

while True:
    ret, frame = video_cap.read()

    if not ret:
        print("End of the video file...")
        break

    if frame_count % 3 == 0:  # Detect every 3rd frame
        # Run YOLO model on the frame
        results = model(frame)

        # Draw bounding boxes for detected vehicles
        for result in results:
            for data in result.boxes.data.tolist():
                x1, y1, x2, y2, confidence, class_id = data
                if confidence > 0.5 and class_id == 2:  # Adjust confidence threshold and class_id for vehicles
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

    # Initialize variables for counting
    counter = 0

    # Count vehicles in each frame
    for result in results:
        for data in result.boxes.data.tolist():
            x1, y1, x2, y2, confidence, class_id = data
            if confidence > 0.5 and class_id == 2:  # Adjust confidence threshold and class_id for vehicles
                counter += 1

    # Display the count of vehicles on every frame
    cv2.putText(frame, f"Vehicles: {counter}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    frame_count += 1

    cv2.imshow("Detected Vehicles", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

end_time = time.time()
elapsed_time = end_time - start_time
fps = frame_count / elapsed_time
print(f"Average FPS: {fps}")

video_cap.release()
cv2.destroyAllWindows()
