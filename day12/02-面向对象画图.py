import turtle


class SacredPattern(turtle.Turtle):
    """绘制宗门秘传图案"""

    def __init__(self):
        super().__init__()
        self.speed(0)
        self.color("cyan")

    def draw_lotus(self, petals=8):
        """绘制灵力莲花"""
        for _ in range(petals):
            self.circle(50, 60)
            self.left(120)
            self.circle(50, 60)
            self.left(120)
            self.right(360 / petals)


# 使用示例
lotus = SacredPattern()
lotus.draw_lotus()
turtle.done()
