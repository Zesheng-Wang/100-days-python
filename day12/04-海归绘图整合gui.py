from tkinter import *
import turtle
from turtle import RawTurtle

class TurtleCanvas:
    """将海龟绘图嵌入GUI"""
    def __init__(self, master):
        self.canvas = Canvas(master)
        self.canvas.pack(side=RIGHT)

        # 在Canvas中创建海龟
        self.t = RawTurtle(self.canvas)
        self.t.speed(0)

        # 控制面板
        control_frame = Frame(master)
        control_frame.pack(side=LEFT)

        Button(control_frame, text="画圆", command=self.draw_circle).pack()
        Button(control_frame, text="清空", command=self.clear).pack()

    def draw_circle(self):
        self.t.color("red")
        self.t.circle(50)

    def clear(self):
        self.t.reset()

# 使用示例
root = Tk()
app = TurtleCanvas(root)
root.mainloop()
