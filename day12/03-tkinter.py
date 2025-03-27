from tkinter import *


class SectGUI:
    def __init__(self):
        self.window = Tk()
        self.window.title("青云宗管理系统")

        # 组件布局
        Label(self.window, text="弟子姓名:").grid(row=0, column=0)
        self.name_entry = Entry(self.window)
        self.name_entry.grid(row=0, column=1)

        Button(self.window, text="录入", command=self.add_disciple).grid(
            row=1, columnspan=2
        )

        # 弟子列表
        self.listbox = Listbox(self.window)
        self.listbox.grid(row=2, columnspan=2)

        self.window.mainloop()

    def add_disciple(self):
        name = self.name_entry.get()
        self.listbox.insert(END, name)
        self.name_entry.delete(0, END)


# 启动GUI
if __name__ == "__main__":
    SectGUI()
