import os
from time import sleep

from circle import Circle


def update_cmd_frame():
    os.system("cls" if os.name == "nt" else "clear")


def main_loop():
    while True:
        print("------------")
        update_cmd_frame()


circle = Circle(50, 9)
# circle.test_rotate(20)

circle.draw()
while True:
    circle.rotate_random()
    sleep(0.01)
    update_cmd_frame()
    sleep(0.01)
# circle.get_height_offsets()
# # main_loop()
