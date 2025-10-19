import os
from time import sleep

from circle import Circle
from drawer import Drawer

circle1 = Circle(61, 8, 1)
circle2 = Circle(61, 6, 1)
circle3 = Circle(31, 4, 1)

drawer = Drawer([circle1, circle2, circle3])


def rotate_loop():
    while True:
        drawer.rotate_random()


rotate_loop()
