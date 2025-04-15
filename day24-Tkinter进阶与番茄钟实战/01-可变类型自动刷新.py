import tkinter as tk
from tkinter import ttk


def start_counter():
    """动态计数器演示"""
    counter = tk.IntVar(value=0)  # 可变整型变量

    def update():
        counter.set(counter.get() + 1)
        root.after(1000, update)  # 定时回调

    label = ttk.Label(root, textvariable=counter)  # 自动绑定
    label.pack(pady=20)
    update()  # 启动循环


root = tk.Tk()
ttk.Button(root, text="启动动态计数器", command=start_counter).pack(pady=50)
root.mainloop()
