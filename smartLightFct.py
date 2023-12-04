import time
from multiprocessing import Process

current_light = 0
priority = 0
avarage_priority_point = 5

def get_new_color(nb_car):
    """
    This function creates a new color for the light depending on the number of people and cars
    
    :param nb_people: number of people
    :param nb_car: number of cars
    :return: a tuple containing the new color for the light, if 0 then no priority, if 1 then priority to people, if 2 then priority to cars
    """
    if nb_car and avarage_priority_point:
        if nb_car/avarage_priority_point >= 1.75:
            return 2
        if nb_car/avarage_priority_point <= 0.25:
            return 1
    return 0

def send_light_color_instruction(priority, current_light=current_light):
    """
    Based on the priority it will change the color of the light

    :param priority: the priority of the light
    
    :param current_light: the current light (0 for green, 1 for yellow, 2 for red)
    """
    if priority == 0:
        None
    if priority == 1 and current_light == 0:
        time.sleep(6)
        current_light = 1
        time.sleep(3)
        current_light = 2
        time.sleep(3)
        current_light = 3
    elif priority == 2 and current_light == 2:
        time.sleep(2)
        current_light = 1

"""Function in case if user want to change priority point remotely"""
def change_priority_point(new_priority):
    avarage_priority_point = new_priority
    