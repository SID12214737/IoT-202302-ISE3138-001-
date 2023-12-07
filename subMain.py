# from object_detection_function import detection
from object_detection_function_everyNth import detection
# import custom stack
from container import FixedSizeStack
# import multiprocessing
from multiprocessing import Process, Value



if __name__ == "__main__":

    # Create a Queue instance
    data_queue = FixedSizeStack(5)

    # Video source path
    vid_source = "1.mp4"

    # Create a multiprocessing queue
    data_queue = FixedSizeStack(max_size=5)

    # Start object detection process
    obj_detect_process = Process(target=detection, args=(data_queue, vid_source))
    obj_detect_process.start()

    

    # Join processes (terminate them when the main process exits)
    obj_detect_process.join()
   