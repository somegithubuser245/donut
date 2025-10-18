from enum import Enum
import math

FUNCTION_QUARTILES_MULTIPLIKATOR = [(1, 1), (1, -1), (-1, -1), (-1, 1)]


class Grade(Enum):
    HIGH = "@"
    MEDIUM = "="
    LOW = "+"
    TINY = "/"
    BARELY = "-"


def get_grade_by_increment(increment: int, depth: int):
    # grade_length = len(Grade.__members__.values())
    # modulo = depth // grade_length if depth > grade_length else depth

    # increment % modulo
    pass


class Vector:
    def __init__(self, x: float, y: float, z: float, grade: Grade):
        self.x = x
        self.y = y
        self.z = z
        self.grade: Grade = grade

    def rotate_across_y(self, angle) -> "Vector":
        x, z = self.rotate_across_line(angle, horizontal=self.x, vertical=self.z)

        return Vector(x, self.y, z, self.grade)

    def rotate_across_x(self, angle) -> "Vector":
        z, y = self.rotate_across_line(angle, horizontal=self.z, vertical=self.y)

        return Vector(self.x, y, z, self.grade)

    def rotate_across_z(self, angle) -> "Vector":
        x, y = self.rotate_across_line(angle, horizontal=self.x, vertical=self.y)

        return Vector(x, y, self.z, self.grade)

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
    def __init__(self, dimension: int, depth: int, granularity: int):
        self.depth = depth
        self.dimension = dimension
        self.radius = dimension // 2
        self.vector_coordinates: list[Vector] = []
        self.output2D = []
        self.granularity = granularity

        self.reset_all_computed()
        self.init_coordinates_inner_circle()

    def reset_all_computed(self):
        self.output2D.clear()
        self.output2D = [
            [" " for i in range(self.dimension)] for _ in range(self.dimension)
        ]

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

    def init_coordinates_inner_circle(self):
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

                grade_index = (increment // self.granularity) - (self.depth // 2)
                pivoted = Vector(x, y, z, grades_list[grade_index]).rotate_across_z(
                    rotate_angle
                )
                self.append_circle_coordinates(pivoted)

    def rotate(self, degrees):
        result = []
        for vector in self.vector_coordinates:
            rotated = vector.rotate_across_y(degrees)
            rotated = rotated.rotate_across_x(degrees)
            result.append(rotated)

        self.vector_coordinates.clear()
        self.vector_coordinates = result.copy()
        self.reset_all_computed()

    def append_circle_coordinates(self, vector: Vector) -> None:
        self.vector_coordinates.append(vector)

    def draw(self):
        z_buffer = [
            [None for _ in range(self.dimension)] for _ in range(self.dimension)
        ]
        for vector in self.vector_coordinates:
            array_end_x = -1 if vector.x > 0 else 0
            array_end_y = -1 if vector.y > 0 else 0

            x = self.radius + round(vector.x) + array_end_x
            y = self.radius + round(vector.y) + array_end_y

            current_z = vector.z

            if (old_z := z_buffer[x][y]) and old_z < current_z:
                continue

            z_buffer[x][y] = current_z

            self.output2D[y][x] = vector.grade.value

        for row in self.output2D:
            print(" ".join(row))

        print("\n")

    def rotate_random(self):
        self.rotate(2)
        self.draw()
