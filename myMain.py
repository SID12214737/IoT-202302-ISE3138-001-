import cv2
import queue
import datetime
import threading
# from object_detection_function import detection
from object_detection_function_everyNth import detection
from conversation.listener import listener
from container import FixedSizeStack

# Create a Queue instance
data_queue = FixedSizeStack(5)

# Video source path
vid_source = "1.mp4"

obj_detect_thread = threading.Thread(target=detection, args=(data_queue, vid_source,))
listen_thread = threading.Thread(target=listener, args=(data_queue,))

obj_detect_thread.start()
listen_thread.start()