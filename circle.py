from enum import Enum
import math

FUNCTION_QUARTILES_MULTIPLIKATOR = [(1, 1), (1, -1), (-1, -1), (-1, 1)]


class Grade(Enum):
    HIGH_2 = "@"
    HIGH_1 = "$"
    HIGH_0 = "#"
    MEDIUM_2 = "="
    MEDIUM_1 = "!"
    MEDIUM_0 = "*"
    LOW_2 = "~"
    LOW_1 = ";"
    LOW_0 = "."
    BLANK = ""


class Vector:
    def __init__(self, x: float, y: float, z: float, grade: Grade | None = None):
        self.x = x
        self.y = y
        self.z = z
        self.unit = None
        self.grade: Grade = grade
    
    def set_unit(self, unit: "Vector") -> None:
        self.unit = unit

    def compute_unit(self, from_vector: "Vector") -> "Vector":
        diff = self.substract(from_vector)
        denom = self._get_denom(diff)
        
        diff.x /= denom
        diff.y /= denom
        diff.z /= denom

        return diff

    def cross(self, another: "Vector") -> float:
        return self.x * another.x + self.y * another.y + self.z * another.z

    # this can probably be done much quicker and better!
    def rotate_across_y(self, angle) -> None:
        self.x, self.z = self.rotate_across_line(
            angle, horizontal=self.x, vertical=self.z
        )

        if self.unit:
            self.unit.x, self.unit.z = self.rotate_across_line(
                angle, horizontal=self.unit.x, vertical=self.unit.z
            )

    def rotate_across_x(self, angle) -> None:
        self.z, self.y = self.rotate_across_line(
            angle, horizontal=self.z, vertical=self.y
        )

        if self.unit:
            self.unit.z, self.unit.y = self.rotate_across_line(
                angle, horizontal=self.unit.z, vertical=self.unit.y
            )

    def rotate_across_z(self, angle) -> None:
        self.x, self.y = self.rotate_across_line(
            angle, horizontal=self.x, vertical=self.y
        )

        if self.unit:
            self.unit.x, self.unit.y = self.rotate_across_line(
                angle, horizontal=self.unit.x, vertical=self.unit.y
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

    def substract(self, another: "Vector") -> "Vector":
        x = another.x - self.x
        y = another.y - self.y
        z = another.z - self.z

        return Vector(x, y, z)
    
    def _get_denom(self, vector: "Vector") -> float:
        return math.sqrt(vector.x ** 2 + vector.y ** 2 + vector.z ** 2)

    def __repr__(self) -> str:
        return f"x: {self.x}, y: {self.y}, z: {self.z}"


class Circle:
    def __init__(self, dimension: int, depth: int, precision_per_pixel: int):
        self.depth = depth
        self.dimension = dimension
        self.radius = dimension // 2

        self.vector_coordinates: list[Vector] = []
        self.granularity = precision_per_pixel

        self.init_inner_circle()

    def get_circle_coordinates(self, edge_end, border_offset: int) -> list[float]:
        height_offsets = []
        offset_from_center = edge_end - border_offset

        for offset in range(0, offset_from_center + 1):
            # some strange granularity creation (i.e. greater circle has more points)
            for granular_divider in range(self.granularity):
                granular_offset = offset + (granular_divider / self.granularity)
                cell_height_from_offset = math.sqrt(
                    abs(offset_from_center**2 - granular_offset**2)
                )
                height_offsets.append((offset, cell_height_from_offset))

        return height_offsets

    def outer_circle_angle(self, x, y, quadrant_symbol):
        if y == 0:
            return math.pi / 2

        angle = math.atan(x / y)
        angle = quadrant_symbol * ((math.pi / 2) - angle)

        return math.degrees(angle)

    def init_inner_circle(self):
        inner_circle_offsets = self.get_circle_coordinates(self.radius, self.depth // 2)

        for muls in FUNCTION_QUARTILES_MULTIPLIKATOR:
            mul_x, mul_y = muls
            for offset_x, offset_y in inner_circle_offsets:
                # coordinates are 0, 0, 0 at the center of the space
                x = offset_x * mul_x
                y = offset_y * mul_y
                quadrant_product = mul_x * mul_y
                rotate_angle = self.outer_circle_angle(offset_x, offset_y, quadrant_product)

                center_vector = Vector(x, y, 0)
                self.init_donut_shape(center_vector, rotate_angle)

    def init_donut_shape(
        self, center_vector: Vector, rotate_angle: float
    ):
        local_offsets = self.get_circle_coordinates(self.depth // 2, 0)
        grades_list = list(Grade.__members__.values())
        for muls in FUNCTION_QUARTILES_MULTIPLIKATOR:
            mul_z, mul_y = muls

            for offset_z, offset_y in local_offsets:
                x = center_vector.x
                z = offset_z * mul_z
                y = center_vector.y + offset_y * mul_y

                vector = Vector(x, y, z)
                
                unit = vector.compute_unit(center_vector)
                vector.set_unit(unit)

                vector.rotate_across_z(rotate_angle)
                self.append_circle_coordinates(vector)

    def rotate(self, x, y, z):
        for vector in self.vector_coordinates:
            vector.rotate_across_x(x)
            vector.rotate_across_y(y)
            vector.rotate_across_z(z)

    def append_circle_coordinates(self, vector: Vector) -> None:
        self.vector_coordinates.append(vector)
