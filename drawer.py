import os
import random
import time
from circle import Circle


class Drawer:
    def __init__(self, circles: list[Circle]):
        self.circles = circles
        dimension = max([circle.dimension for circle in circles])

        self.dimension = dimension
        self.center = dimension // 2
        self.output2D = []
        self.z_buffer = []
        self.reset_all_computed()

    def reset_all_computed(self):
        self.output2D.clear()
        self.z_buffer.clear()
        self.z_buffer = [
            [None for _ in range(self.dimension)] for _ in range(self.dimension)
        ]
        self.output2D = [
            [" " for i in range(self.dimension)] for _ in range(self.dimension)
        ]

    def rotate_random(self):
        r = random.Random()
        angle_range = [10, 90]

        angle_x = r.randint(*angle_range)
        angle_y = r.randint(*angle_range)
        angle_z = r.randint(*angle_range)

        for i in range(1, angle_range[1]):
            x = angle_x / angle_range[0]
            y = angle_y / angle_range[0]
            z = angle_z / angle_range[0]

            for index, circle in enumerate(self.circles):
                mult = (-1) ** index

                x *= mult
                y *= mult
                z *= mult

                self.rotate_circle(circle, x, y, z)
                self.draw(circle)

            self.print_drawing()
            self.reset_all_computed()
            time.sleep(0.05)
            self.update_cmd_frame()
            # time.sleep(0.03)

    def rotate_circle(self, circle: Circle, x, y, z):
        circle.rotate(x, y, z)

    def update_cmd_frame(self):
        os.system("cls" if os.name == "nt" else "clear")

    def draw(self, circle: Circle):
        for vector in circle.vector_coordinates:
            array_end_x = -1 if vector.x > 0 else 0
            array_end_y = -1 if vector.y > 0 else 0

            x = self.center + round(vector.x) + array_end_x
            y = self.center + round(vector.y) + array_end_y

            current_z = vector.z

            if (old_z := self.z_buffer[x][y]) and old_z < current_z:
                continue

            self.z_buffer[x][y] = current_z

            self.output2D[y][x] = vector.grade.value

    def print_drawing(self):
        for row in self.output2D:
            print(".".join(row))
