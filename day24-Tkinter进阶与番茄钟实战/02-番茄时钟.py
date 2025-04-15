# 导入必要的库
import tkinter as tk  # 导入GUI库
from tkinter import ttk  # 导入tkinter的增强组件
import pystray  # 系统托盘库
from PIL import Image, ImageDraw  # 图像处理库（用于创建托盘图标）
import threading  # 多线程支持

class TomatoTimer:
    def __init__(self, master):
        """番茄钟计时器核心类"""
        self.master = master  # 主窗口对象
        self.time_left = tk.IntVar(value=25 * 60)  # 剩余时间变量（默认25分钟）
        self.is_running = False  # 计时器运行状态标志

        # 时间显示标签
        self.time_label = ttk.Label(
            master, 
            textvariable=self.time_left,  # 绑定到时间变量
            font=("Helvetica", 48)  # 设置大字体
        )
        self.time_label.pack(pady=20)  # 放置标签并添加垂直间距

        # 按钮框架容器
        self.btn_frame = ttk.Frame(master)
        self.btn_frame.pack()
        
        # 开始/暂停按钮
        ttk.Button(
            self.btn_frame, 
            text="开始", 
            command=self.start  # 绑定启动方法
        ).pack(side="left")  # 左对齐
        
        # 重置按钮
        ttk.Button(
            self.btn_frame, 
            text="重置", 
            command=self.reset  # 绑定重置方法
        ).pack(side="left")  # 左对齐

    def start(self):
        """启动/暂停计时器"""
        self.is_running = not self.is_running  # 切换运行状态
        if self.is_running:
            self.countdown()  # 如果正在运行则开始倒计时

    def reset(self):
        """重置计时器到初始状态"""
        self.is_running = False  # 停止计时
        self.time_left.set(25 * 60)  # 重置为25分钟

    def countdown(self):
        """倒计时核心逻辑"""
        if self.is_running and self.time_left.get() > 0:
            self.time_left.set(self.time_left.get() - 1)  # 秒数减1
            self.master.after(1000, self.countdown)  # 1秒后递归调用
        elif self.time_left.get() == 0:
            self.show_notification()  # 时间为0时显示通知

    def show_notification(self):
        """显示时间到通知"""
        self.master.iconify()  # 最小化主窗口
        self.master.bell()  # 播放系统提示音
        
        # 创建弹出窗口
        popup = tk.Toplevel()
        popup.title("时间到！")
        ttk.Label(popup, text="🍅 该休息啦！").pack(pady=20)  # 添加标签
        ttk.Button(popup, text="好的", command=popup.destroy).pack()  # 关闭按钮


class SystemTray:
    """系统托盘图标管理类"""
    def __init__(self, master):
        self.master = master  # 主窗口引用
        self.icon = self.create_icon()  # 创建托盘图标
        self.menu = pystray.Menu(  # 创建托盘菜单
            pystray.MenuItem("显示主界面", self.show_window),  # 菜单项1
            pystray.MenuItem("退出程序", self.quit)  # 菜单项2
        )
        # 创建托盘图标实例
        self.tray = pystray.Icon(
            "tomato_timer",  # 图标名称
            self.icon,  # 图标图像
            "番茄钟",  # 悬停提示文本
            self.menu  # 关联菜单
        )
        
        # 在新线程中运行托盘图标（避免阻塞主线程）
        self.thread = threading.Thread(target=self.tray.run, daemon=True)
        self.thread.start()

    def create_icon(self):
        """创建简单的红色方块托盘图标"""
        image = Image.new('RGB', (64, 64), (255, 255, 255))  # 创建白色背景图像
        dc = ImageDraw.Draw(image)  # 获取绘图对象
        dc.rectangle((16, 16, 48, 48), fill='red')  # 绘制红色方块
        return image

    def show_window(self, icon, item):
        """显示主窗口的回调函数"""
        self.master.after(0, self.master.deiconify)  # 在主线程中恢复窗口

    def quit(self, icon, item):
        """退出程序的回调函数"""
        self.master.after(0, self.master.destroy)  # 在主线程中销毁窗口


class TomatoApp(tk.Tk):
    """主应用程序类"""
    def __init__(self):
        super().__init__()
        self.title("番茄修仙钟")  # 设置窗口标题
        self.geometry("300x250")  # 设置窗口大小
        # 设置窗口关闭按钮行为（最小化到托盘）
        self.protocol("WM_DELETE_WINDOW", self.minimize_to_tray)

        # 初始化组件
        self.timer = TomatoTimer(self)  # 创建计时器实例
        self.tray = SystemTray(self)  # 创建托盘图标实例

        # 样式配置
        self.style = ttk.Style()
        self.style.configure("TButton", font=("微软雅黑", 12))  # 按钮字体
        self.style.configure("Red.TButton", foreground="red")  # 红色按钮样式

    def minimize_to_tray(self):
        """最小化到托盘的方法"""
        self.withdraw()  # 隐藏主窗口

    def run(self):
        """启动主循环"""
        self.mainloop()


if __name__ == "__main__":
    app = TomatoApp()  # 创建应用实例
    app.run()  # 运行应用