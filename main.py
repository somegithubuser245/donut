import os
from time import sleep

from circle import Circle
from drawer import Drawer

circle1 = Circle(41, 10, 2)

drawer = Drawer([circle1])


def rotate_loop():
    while True:
        drawer.rotate_random()


rotate_loop()
