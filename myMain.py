import RPi.GPIO as GPIO
# from object_detection_function import detection
from object_detection_function_everyNth import detection
# import listener
from conversation.listener import listener
# import custom stack
from container import FixedSizeStack
import time
# import multiprocessing
from multiprocessing import Process, Value

# import traffic light class
from smartLightFct import TrafficLightController

def simulate_traffic(controller):
    # Simulating changes in the number of cars
    while True:
        # This is just an example; replace this with your actual car count logic
        time.sleep(5)
        cars_count = data_queue.get()  # Replace this with your car count logic
        new_color = controller.get_new_color(cars_count)
        controller.change_light(new_color)

if __name__ == "__main__":

    # create Trffic light instance
    controller = TrafficLightController()
    # Create a Queue instance
    data_queue = FixedSizeStack(5)

    # Video source path
    vid_source = "1.mp4"

    # Create a multiprocessing queue
    data_queue = FixedSizeStack(max_size=5)

    # Start object detection process
    obj_detect_process = Process(target=detection, args=(data_queue, vid_source))
    obj_detect_process.start()

    # Start listener process
    listen_process = Process(target=listener, args=(data_queue,))
    listen_process.start()

    # Start traffic light control process
    traffic_process = Process(target=simulate_traffic, args=(controller,))
    traffic_process.start()

    # Join processes (terminate them when the main process exits)
    obj_detect_process.join()
    listen_process.join()
    traffic_process.join()

    # Modify priority remotely (for demonstration purposes)
    controller.change_priority_point(10.0)
    time.sleep(20)  # Let the simulation run for a while before changing priority
    controller.change_priority_point(6.0)
    
    # Clean up GPIO before exiting
    GPIO.cleanup()
