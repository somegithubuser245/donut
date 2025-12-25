import os
import random
import time
from circle import Circle, Grade, Vector


class Drawer:
    def __init__(self, circles: list[Circle]):
        self.circles = circles
        dimension = max([circle.dimension for circle in circles])

        self.dimension = dimension
        self.center = dimension // 2
        self.output2D = []
        self.z_buffer = []
        self.camera = Vector(0, -dimension, -dimension)
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
        direction = r.randint(1, 2)
        direction = (-1) ** direction
        for _ in range(len(self.circles)):
            angle_x = r.randint(*angle_range) * direction
            angle_y = r.randint(*angle_range) * direction
            angle_z = r.randint(*angle_range) * direction

            angles_vector = Vector(angle_x, angle_y, angle_z)
            random_angles.append(angles_vector)

        return random_angles

    def rotate_random(self):
        angle_range = [30, 90]
        rand_angles = self.create_random_angles(angle_range)
        frame_angle_divider = angle_range[0] // 2

        for _ in range(1, angle_range[1]):
            for index, circle in enumerate(self.circles):
                x = rand_angles[index].x / frame_angle_divider
                y = rand_angles[index].y / frame_angle_divider
                z = rand_angles[index].z / frame_angle_divider

                self.rotate_circle(circle, x, y, z)
                self.draw(circle)

            self.print_drawing()
            self.reset_all_computed()
            time.sleep(0.1)
            self.update_cmd_frame()

    def rotate_circle(self, circle: Circle, x, y, z):
        circle.rotate(x, y, z)

    def update_cmd_frame(self):
        os.system("cls" if os.name == "nt" else "clear")

    def get_grade(self, dot_product: float) -> Grade:
        if -0.1 < dot_product <= 0:
            return Grade.LOW_0
        if -0.2 < dot_product <= -0.1:
            return Grade.LOW_1
        if -0.3 < dot_product <= -0.2:
            return Grade.LOW_2
        if -0.3 < dot_product <= -0.4:
            return Grade.MEDIUM_0
        if -0.6 < dot_product <= -0.5:
            return Grade.MEDIUM_1
        if -0.7 < dot_product <= -0.6:
            return Grade.MEDIUM_2
        if -0.8 < dot_product <= -0.7:
            return Grade.HIGH_0
        if -0.9 < dot_product <= -0.8:
            return Grade.HIGH_1
        if -1 <= dot_product <= -0.9:
            return Grade.HIGH_2
    
        return Grade.LOW_0

    def draw(self, circle: Circle):
        for vector in circle.vector_coordinates:
            # self.camera.x, self.camera.y = vector.x, vector.y
            cam_to_donut_unit = vector.compute_unit(self.camera)
            dot = vector.unit.cross(cam_to_donut_unit)
            
            vector.grade = self.get_grade(dot)
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
            print(" ".join(row))
