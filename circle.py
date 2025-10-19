from enum import Enum
import math
import os
import random
import time

FUNCTION_QUARTILES_MULTIPLIKATOR = [(1, 1), (1, -1), (-1, -1), (-1, 1)]


class Grade(Enum):
    HIGH = "@"
    MEDIUM = "="
    LOW = "/"
    TINY = "|"
    BARELY = "-"


def get_grade_by_increment(increment: int, depth: int):
    # grade_length = len(Grade.__members__.values())
    # modulo = depth // grade_length if depth > grade_length else depth

    # increment % modulo
    pass


class Vector:
    def __init__(self, x: float, y: float, z: float, grade: Grade | None = None):
        self.x = x
        self.y = y
        self.z = z
        self.grade: Grade = grade

    def rotate_across_y(self, angle) -> None:
        self.x, self.z = self.rotate_across_line(
            angle, horizontal=self.x, vertical=self.z
        )

    def rotate_across_x(self, angle) -> None:
        self.z, self.y = self.rotate_across_line(
            angle, horizontal=self.z, vertical=self.y
        )

    def rotate_across_z(self, angle) -> None:
        self.x, self.y = self.rotate_across_line(
            angle, horizontal=self.x, vertical=self.y
        )

    def rotate_across_line(self, angle, horizontal: float, vertical: float):
        angle_radians = math.radians(angle)

        h_teta = horizontal * math.cos(angle_radians) - vertical * math.sin(
            angle_radians
        )
        v_teta = vertical * math.cos(angle_radians) + horizontal * math.sin(
            angle_radians
        )

        return h_teta, v_teta

    def __repr__(self) -> str:
        return f"x: {self.x}, y: {self.y}, z: {self.z}"


class Circle:
    def __init__(self, dimension: int, depth: int, precision_per_pixel: int):
        self.depth = depth
        self.dimension = dimension
        self.radius = dimension // 2

        self.vector_coordinates: list[Vector] = []
        self.granularity = precision_per_pixel

        self.init_coordinates()

    def get_circle_coordinates(self, edge_end, border_offset: int) -> list[float]:
        height_offsets = []
        offset_from_center = edge_end - border_offset

        for offset in range(0, offset_from_center + 1):
            for granular_divider in range(self.granularity):
                granular_offset = offset + (granular_divider / self.granularity)
                cell_height_from_offset = math.sqrt(
                    abs(offset_from_center**2 - granular_offset**2)
                )
                height_offsets.append((offset, cell_height_from_offset))

        return height_offsets

    def outer_circle_angle(self, x, y, quart_symbol):
        if y == 0:
            return math.pi / 2

        angle = math.atan(x / y)

        angle = quart_symbol * ((math.pi / 2) - angle)

        return math.degrees(angle)

    def init_coordinates(self):
        inner_circle_offsets = self.get_circle_coordinates(self.radius, self.depth // 2)

        for muls in FUNCTION_QUARTILES_MULTIPLIKATOR:
            mul_x, mul_y = muls
            for offset_x, offset_y in inner_circle_offsets:
                # coordinates are 0, 0, 0 at the center of the space
                x = offset_x * mul_x
                y = offset_y * mul_y
                qaurt_symbol = mul_x * mul_y
                rotate_angle = self.outer_circle_angle(offset_x, offset_y, qaurt_symbol)
                self.init_depth_coordinates(x, y, rotate_angle)

    def init_depth_coordinates(
        self, x_inner: float, y_inner: float, rotate_angle: float
    ):
        local_offsets = self.get_circle_coordinates(self.depth // 2, 0)
        grades_list = list(Grade.__members__.values())
        for muls in FUNCTION_QUARTILES_MULTIPLIKATOR:
            mul_x, mul_y = muls

            for increment, offsets in enumerate(local_offsets):
                offset_z, offset_y = offsets

                x = x_inner
                z = offset_z * mul_x
                y = y_inner + offset_y * mul_y

                grade_index = (self.depth // 2) - (increment // self.granularity)

                vector = Vector(x, y, z, grades_list[grade_index])
                vector.rotate_across_z(rotate_angle)
                self.append_circle_coordinates(vector)

    def rotate(self, x, y, z):
        for vector in self.vector_coordinates:
            vector.rotate_across_x(x)
            vector.rotate_across_y(y)
            vector.rotate_across_z(z)

    def append_circle_coordinates(self, vector: Vector) -> None:
        self.vector_coordinates.append(vector)
