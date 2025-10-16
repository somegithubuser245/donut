import math


class Circle:
    def __init__(self, dimension: int):
        self.plane = [[" " for i in range(dimension)] for _ in range(dimension)]
        self.dimension = dimension
        self.radius = dimension // 2
        self.center = dimension // 2

    def get_height_offsets(self) -> list[int]:
        height_offsets = []

        for offset in range(0, self.radius + 1):
            cell_height_from_offset = math.sqrt(abs(self.radius**2 - offset**2))
            cell_height_from_offset = round(cell_height_from_offset)
            height_offsets.append(cell_height_from_offset)

        return height_offsets

    def render_circle(self):
        circle_parts_multiplicators = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
        offsets_y = self.get_height_offsets()
        border_char = "+."

        for muls in circle_parts_multiplicators:
            mul_x, mul_y = muls
            for offsets in enumerate(offsets_y):
                offset_x, offset_y = offsets

                border_x = self.center + (offset_x * mul_x)
                border_y = self.center + (offset_y * mul_y)

                border_x = border_x - 1 if mul_x > 0 else border_x
                border_y = border_y - 1 if mul_y > 0 else border_y

                self.plane[border_x][border_y] = border_char

    def draw(self):
        self.render_circle()
        # self.draw_circle()
        for row_enum in enumerate(self.plane):
            index, row = row_enum
            print(f"{'.'.join(row)}")
