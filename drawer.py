import os
import random
import time
from circle import Circle, Vector


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

    def create_random_angles(self, angle_range: list[int]) -> list[Vector]:
        r = random.Random()
        random_angles = []
        direction_rand = r.randint(1, 2)
        direction_rand = (-1) ** direction_rand
        for _ in range(len(self.circles)):
            angle_x = r.randint(*angle_range) * direction_rand
            angle_y = r.randint(*angle_range) * direction_rand
            angle_z = r.randint(*angle_range) * direction_rand

            angles_vector = Vector(angle_x, angle_y, angle_z)
            random_angles.append(angles_vector)

        return random_angles

    def rotate_random(self):
        angle_range = [30, 90]
        rand_vectors = self.create_random_angles(angle_range)
        frame_angle_divider = angle_range[0] // 2

        for _ in range(1, angle_range[1]):
            for index, circle in enumerate(self.circles):
                x = rand_vectors[index].x / frame_angle_divider
                y = rand_vectors[index].y / frame_angle_divider
                z = rand_vectors[index].z / frame_angle_divider

                self.rotate_circle(circle, x, y, z)
                self.draw(circle)

            self.print_drawing()
            self.reset_all_computed()
            time.sleep(0.05)
            self.update_cmd_frame()

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
