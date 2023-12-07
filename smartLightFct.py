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
        
        if color == 1:  # Green
            GPIO.output(self.GREEN_PIN, GPIO.HIGH)
        elif color == 2:  # Yellow
            GPIO.output(self.YELLOW_PIN, GPIO.HIGH)
        elif color == 3:  # Red
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

        if priority == 1:
            # Priority for cars: Give more time for Green light
            self.change_light(0)  # Green
            time.sleep(8)
            self.change_light(2)  # Red
        elif priority == 2:
            # Priority for people: Give more time for Red light
            self.change_light(1)  # Yellow
            time.sleep(4)
            self.change_light(0)  # Green
            time.sleep(2)
            self.change_light(2)  # Red
        else:
            # No priority: Normal operation
            self.change_light(0)  # Green
            time.sleep(4)
            self.change_light(1)  # Yellow
            time.sleep(2)
            self.change_light(2)  # Red
            
    def change_priority_point(self, new_priority):
        self.average_priority_point = new_priority
