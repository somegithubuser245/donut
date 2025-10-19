import os
from time import sleep

from circle import Circle
from drawer import Drawer

circle1 = Circle(51, 8, 2)
circle2 = Circle(51, 6, 2)
# circle3 = Circle(15, 3, 3)

drawer = Drawer([circle1, circle2])


def rotate_loop():
    while True:
        drawer.rotate_random()


rotate_loop()
