import numpy as np
import datetime
import cv2
from ultralytics import YOLO
from helper import create_video_writer

conf_threshold = 0.4

# Initialize the YOLOv8 model using the default weights
model = YOLO("yolov3-tinyu.pt")

# Class names for mapping class IDs to labels
class_names = {
    0: "person",
    1: "bicycle",
    2: "car",
    3: "motorbike",
    5: "bus",
    7: "truck"
}

def detection(que, cap_source=0, out_des="output.mp4"):
    # Initialize the video capture and the video writer objects
    video_cap = cv2.VideoCapture(cap_source)
    writer = create_video_writer(video_cap, out_des)
    # loop over the frames
    while True:
        # starter time to compute the fps
        start = datetime.datetime.now()
        ret, frame = video_cap.read()
        # if there is no frame, we have reached the end of the video
        if not ret:
            print("No cap data")
            break
        
        # Counter for vehicles in each frame
        total_vehicles = 0
        
        ### Detect the objects in the frame using the YOLO model ###
        # run the YOLO model on the frame
        results = model(frame)
            
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
                # filter out weak predictions by ensuring the confidence is
                # greater than the minimum confidence and only count vehicles
                if confidence > conf_threshold and class_id in class_names:
                    total_vehicles += 1
                    # Add labels (class names) to the bounding boxes
                    label = class_names[class_id]
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        que.put(total_vehicles)  # Put data in the queue
        # end time to compute the fps
        end = datetime.datetime.now()
        # calculate the frame per second and draw it on the frame
        fps = f"FPS: {1 / (end - start).total_seconds():.2f}"
        cv2.putText(frame, fps, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 8)
        
        # Show the total number of vehicles in the frame
        cv2.putText(frame, f"Total Vehicles: {total_vehicles}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # show the output frame
        cv2.imshow("Output", frame)
        # write the frame to disk
        writer.write(frame)
        if cv2.waitKey(1) == ord("q"):
            break

    # release the video capture, video writer, and close all windows
    video_cap.release()
    writer.release()
    cv2.destroyAllWindows()
