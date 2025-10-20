import os
from time import sleep

from circle import Circle
from drawer import Drawer

circle1 = Circle(51, 10, 2)
circle2 = Circle(45, 7, 2)
circle3 = Circle(21, 4, 1)

drawer = Drawer([circle1, circle2, circle3])


def rotate_loop():
    while True:
        drawer.rotate_random()


rotate_loop()
