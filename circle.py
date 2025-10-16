import math


class Vector:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

    def rotate_across_y(self, angle) -> "Vector":
        angle_radians = math.radians(angle)

        x_teta = self.x * math.cos(angle_radians) - self.z * math.sin(angle_radians)
        z_teta = self.z * math.cos(angle_radians) + self.x * math.sin(angle_radians)

        x_teta, z_teta = round(x_teta), round(z_teta)

        return Vector(x_teta, self.y, z_teta)

    def __repr__(self) -> str:
        return f"x: {self.x}, y: {self.y}, z: {self.z}"


class Circle:
    def __init__(self, dimension: int):
        self.dimension = dimension
        self.radius = dimension // 2
        self.center = dimension // 2
        self.vector_coordinates: list[Vector] = []
        self.coordinates = []
        self.output2D = []

        self.reset_all_computed(dimension)
        self.init_coordinates()

    def reset_all_computed(self, dimension):
        self.coordinates = [
            [[False for i in range(dimension)] for _ in range(dimension)]
            for _ in range(dimension)
        ]
        self.output2D = [[" " for i in range(dimension)] for _ in range(dimension)]

    def get_height_offsets(self) -> list[int]:
        height_offsets = []

        for offset in range(0, self.radius + 1):
            cell_height_from_offset = math.sqrt(abs(self.radius**2 - offset**2))
            cell_height_from_offset = round(cell_height_from_offset)
            height_offsets.append(cell_height_from_offset)

        return height_offsets

    def init_coordinates(self):
        circle_parts_multiplicators = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
        offsets_y = self.get_height_offsets()

        for muls in circle_parts_multiplicators:
            mul_x, mul_y = muls
            for offsets in enumerate(offsets_y):
                offset_x, offset_y = offsets

                # coordinates are 0, 0, 0 at the center of the space
                x = offset_x * mul_x
                y = offset_y * mul_y

                self.append_circle_coordinates(x, y, self.center)

    def rotate(self, degrees):
        result = []
        for vector in self.vector_coordinates:
            rotated = vector.rotate_across_y(degrees)
            # print(vector)
            # print(rotated)
            result.append(rotated)

        self.vector_coordinates.clear()
        self.vector_coordinates = result

    def append_circle_coordinates(self, x: int, y: int, z: int) -> None:
        vector = Vector(x, y, z)
        self.vector_coordinates.append(vector)

    def convert_vectors_to_space(self):
        for vector in self.vector_coordinates:
            self.coordinates[vector.x][vector.y][vector.z] = True

    def draw(self):
        self.convert_vectors_to_space()

        for x in range(self.dimension):
            for y in range(self.dimension):
                for z in range(self.dimension):
                    if self.coordinates[x][y][z]:
                        self.output2D[x][y] = "+"

        for row in self.output2D:
            print(".".join(row))

    def test_rotate(self):
        self.draw()
        self.reset_all_computed(self.dimension)
        self.rotate(30)
        self.draw()
