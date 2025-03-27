from tkinter import *
import turtle
from turtle import RawTurtle
from tkinter import colorchooser, filedialog

class SpiritualPainter:
    def __init__(self):
        self.window = Tk()
        self.window.title("灵力轨迹绘制器")

        # 绘图区
        self.canvas = Canvas(self.window, width=600, height=500)
        self.canvas.pack(side=LEFT)
        self.t = RawTurtle(self.canvas)
        self.t.speed(0)

        # 控制面板
        control_frame = Frame(self.window)
        control_frame.pack(side=RIGHT, padx=10)

        # 颜色选择
        self.color_btn = Button(control_frame, text="选择颜色", command=self.choose_color)
        self.color_btn.pack(pady=5)

        # 图形选择
        self.shape_var = StringVar(value="circle")
        OptionMenu(control_frame, self.shape_var,
                  "circle", "star", "spiral").pack(pady=5)

        # 绘制按钮
        Button(control_frame, text="绘制", command=self.draw).pack(pady=5)
        Button(control_frame, text="保存", command=self.save).pack(pady=5)
        Button(control_frame, text="清空", command=self.clear).pack(pady=5)

        self.current_color = "black"

    def choose_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.current_color = color

    def draw(self):
        self.t.color(self.current_color)
        shape = self.shape_var.get()

        if shape == "circle":
            self.t.circle(50)
        elif shape == "star":
            for _ in range(5):
                self.t.forward(100)
                self.t.right(144)
        elif shape == "spiral":
            for i in range(50):
                self.t.forward(i*2)
                self.t.right(91)

    def clear(self):
        self.t.reset()

    def save(self):
        path = filedialog.asksaveasfilename(defaultextension=".eps")
        if path:
            self.canvas.postscript(file=path, colormode='color')

if __name__ == "__main__":
    app = SpiritualPainter()
    app.window.mainloop()
