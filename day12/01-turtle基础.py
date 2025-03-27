import turtle

# 初始化画布
screen = turtle.Screen()
screen.title("修仙图腾")
screen.bgcolor("black")

# 创建画笔
pen = turtle.Turtle()
pen.color("gold")
pen.pensize(3)

# 绘制五行阵
for _ in range(5):
    pen.forward(100)
    pen.right(144)  # 五角星角度

pen.hideturtle()
turtle.done()
