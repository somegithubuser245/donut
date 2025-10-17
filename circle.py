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

        x_teta = round(x_teta)
        z_teta = round(z_teta)

        return Vector(x_teta, self.y, z_teta)

    def __repr__(self) -> str:
        return f"x: {self.x}, y: {self.y}, z: {self.z}"


class Circle:
    def __init__(self, dimension: int):
        self.dimension = dimension
        self.radius = dimension // 2
        self.center_x = dimension // 2
        self.center_y = dimension // 2
        self.vector_coordinates: list[Vector] = []
        self.coordinates = []
        self.output2D = []

        self.reset_all_computed(dimension)
        self.init_coordinates()

    def reset_all_computed(self, dimension):
        self.output2D.clear()
        self.output2D = [["." for i in range(dimension)] for _ in range(dimension)]

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

                self.append_circle_coordinates(x, y, self.radius)

    def rotate(self, degrees):
        max_x, min_x = 0, 0
        result = []
        for vector in self.vector_coordinates:
            rotated = vector.rotate_across_y(degrees)
            result.append(rotated)
            if rotated.x > max_x:
                max_x = rotated.x

            if rotated.x < min_x:
                min_x = rotated.x
            # print(f"v: {vector}")
            # print(f"v': {rotated}")

        print(min_x)
        self.center_x = abs(min_x)
        print(self.center_x)

        self.vector_coordinates.clear()
        self.vector_coordinates = result.copy()

    def append_circle_coordinates(self, x: int, y: int, z: int) -> None:
        vector = Vector(x, y, z)
        self.vector_coordinates.append(vector)

    def draw(self):
        for vector in self.vector_coordinates:
            array_end_x = -1 if vector.x > 0 else 0
            array_end_y = -1 if vector.y > 0 else 0

            x = self.center_x + vector.x + array_end_x
            y = self.center_y + vector.y + array_end_y
            # print(f"pre x: {vector.x} pre y: {vector.y}")
            # print(f"x: {x}, y: {y}")

            self.output2D[y][x] = "+"

        for row in self.output2D:
            print(".".join(row))

        print("\n")

    def test_rotate(self, degrees: int):
        self.rotate(degrees)
        self.draw()
        self.reset_all_computed(self.dimension)
