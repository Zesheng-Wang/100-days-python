class Vector2:
    """二维坐标类"""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


# 方向常量
DIRECTIONS = {
    "up": Vector2(0, 1),
    "down": Vector2(0, -1),
    "left": Vector2(-1, 0),
    "right": Vector2(1, 0),
}
