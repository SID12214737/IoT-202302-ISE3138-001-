import cv2
from ultralytics import YOLO

# Load the YOLO model
model = YOLO("yolov8s.pt")

# Open the video file
# video_cap = cv2.VideoCapture(0)
video_cap = cv2.VideoCapture("traffic35_720.mp4")

frame_count = 0

while True:
    ret, frame = video_cap.read()

    if not ret:
        print("End of the video file...")
        break

    # Run YOLO model on the frame
    results = model(frame)

    # Initialize variables for counting
    counter = 0

    # Extract detections and count vehicles
    for result in results:
        for data in result.boxes.data.tolist():
            x1, y1, x2, y2, confidence, class_id = data
            if confidence > 0.5 and class_id == 2:  # Adjust confidence threshold and class_id for vehicles
                counter += 1
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

    # Display the count of vehicles on the frame
    cv2.putText(frame, f"Vehicles: {counter}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    frame_count += 1

    cv2.imshow("Detected Vehicles", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_cap.release()
cv2.destroyAllWindows()
