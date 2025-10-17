import os
from time import sleep

from circle import Circle


def update_cmd_frame():
    os.system("cls" if os.name == "nt" else "clear")


def main_loop():
    while True:
        print("------------")
        update_cmd_frame()


circle = Circle(27)

# circle.draw()
for i in range(1000):
    circle.test_rotate(30)
    sleep(0.1)
    update_cmd_frame()
# circle.get_height_offsets()
# main_loop()
