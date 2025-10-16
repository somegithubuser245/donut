import os

from circle import Circle


def update_cmd_frame():
    os.system("cls" if os.name == "nt" else "clear")


def main_loop():
    while True:
        print("------------")
        update_cmd_frame()


circle = Circle(21)

circle.draw_circle()
# circle.get_height_offsets()
# main_loop()
