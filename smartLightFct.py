import time
from multiprocessing import Process, Value
import RPi.GPIO as GPIO


class TrafficLightController:
    def __init__(self):
        # Define GPIO pins for red, yellow, and green LEDs
        self.RED_PIN = 17
        self.YELLOW_PIN = 18
        self.GREEN_PIN = 19

        # Set up GPIO mode and pins
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.RED_PIN, GPIO.OUT)
        GPIO.setup(self.YELLOW_PIN, GPIO.OUT)
        GPIO.setup(self.GREEN_PIN, GPIO.OUT)

        # Shared variables
        self.current_light = 0
        self.priority = 0
        self.average_priority_point = 5.0  

    def change_light(self, color):
        GPIO.output(self.RED_PIN, GPIO.LOW)
        GPIO.output(self.YELLOW_PIN, GPIO.LOW)
        GPIO.output(self.GREEN_PIN, GPIO.LOW)
        
        if color == 0:  # Green
            GPIO.output(self.GREEN_PIN, GPIO.HIGH)
        elif color == 1:  # Yellow
            GPIO.output(self.YELLOW_PIN, GPIO.HIGH)
        elif color == 2:  # Red
            GPIO.output(self.RED_PIN, GPIO.HIGH)
        else:
            print("Invalid color parameter")

    def get_new_color(self, nb_car):
        if nb_car and self.average_priority_point:
            if nb_car / self.average_priority_point >= 1.75:
                return 2  # Priority to cars (red)
            if nb_car / self.average_priority_point <= 0.25:
                return 1  # Priority to people (yellow)
        return 0  # No priority (green)

    def send_light_color_instruction(self):
        priority = self.priority
        current_light = self.current_light

        if priority == 1 and current_light == 0:
            time.sleep(6)
            self.change_light(1)
            self.current_light = 1
            time.sleep(3)
            self.change_light(2)
            self.current_light = 2
            time.sleep(3)
            self.change_light(2)  # Assuming 2 for red
            self.current_light = 2
        elif priority == 2 and current_light == 2:
            time.sleep(2)
            self.change_light(1)
            self.current_light = 1

    def change_priority_point(self, new_priority):
        self.average_priority_point = new_priority
