"""
记忆卡间隔重复系统 - 记忆熔炉 v1.2
作者：AI助手
功能说明：
1. 使用tkinter构建的图形界面应用程序
2. 支持卡片正反面翻转动画效果
3. 实现基于SM-2改进的间隔重复算法
4. 记忆曲线可视化功能
5. 自动保存/加载学习进度
"""

# 导入必要的库
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import json
import os
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class FlashCard(tk.Canvas):
    """可翻转的记忆卡片组件"""

    def __init__(self, master, front_text, back_text, **kwargs):
        """
        初始化记忆卡片
        :param master: 父容器
        :param front_text: 正面文字内容
        :param back_text: 背面文字内容
        """
        super().__init__(master, width=300, height=200, bg="white", **kwargs)
        self.front_text = front_text  # 卡片正面内容
        self.back_text = back_text  # 卡片背面内容
        self.is_front = True  # 当前显示是否为正面

        # 初始化绘制卡片正面
        self.draw_card(self.front_text)
        # 绑定点击事件
        self.bind("<Button-1>", self.flip)

    def draw_card(self, text):
        """绘制卡片内容"""
        self.delete("all")  # 清空画布
        # 绘制蓝色边框
        self.create_rectangle(5, 5, 295, 195, outline="#4B8BBE", width=2)
        # 添加文字内容（支持自动换行）
        self.create_text(
            150, 100, text=text, font=("微软雅黑", 14), width=280, tags="text"
        )

    def flip(self, event=None):
        """执行卡片翻转动画"""
        # 使用宽度变化模拟3D翻转效果
        for i in range(0, 90, 5):
            self.configure(width=300 * (1 - abs(i - 45) / 45))  # 动态调整宽度
            self.update()
            self.master.after(20)  # 控制动画速度

        # 切换显示内容
        new_text = self.back_text if self.is_front else self.front_text
        self.is_front = not self.is_front  # 切换正反面状态
        self.draw_card(new_text)


class Card:
    """记忆卡片数据模型"""

    def __init__(self, front, back):
        """
        初始化卡片数据
        :param front: 正面内容
        :param back: 背面内容
        """
        self.front = front  # 卡片正面问题
        self.back = back  # 卡片背面答案
        self.interval = 1  # 当前复习间隔（天）
        self.ease_factor = 2.5  # 易度因子（调整间隔用）
        self.next_review = datetime.now()  # 下次复习时间
        self.review_count = 0  # 总复习次数
        self.history = []  # 复习历史记录（日期，评分）


class SpacedRepetition:
    """间隔重复调度算法（基于SM-2改进）"""

    def update_card(self, card, quality):
        """
        更新卡片记忆参数
        :param card: 要更新的卡片对象
        :param quality: 用户评分（0-3）
        """
        # 评分对应参数映射表（易度调整值，间隔调整系数）
        quality_map = {
            0: (0.0, 0.8),  # 忘记
            1: (0.4, 0.9),  # 困难
            2: (0.6, 1.1),  # 一般
            3: (1.0, 1.3),  # 容易
        }

        # 获取调整参数
        ease_delta, interval_mod = quality_map.get(quality, (0, 1))
        # 调整易度因子（最低1.3）
        card.ease_factor = max(1.3, card.ease_factor + ease_delta)
        # 计算新间隔（取整）
        card.interval = int(round(card.interval * card.ease_factor * interval_mod))
        # 设置下次复习时间
        card.next_review = datetime.now() + timedelta(days=card.interval)
        card.review_count += 1  # 增加复习次数
        # 记录复习历史
        card.history.append((datetime.now().strftime("%Y-%m-%d"), quality))


class FlashCardApp(tk.Tk):
    """主应用程序"""

    def __init__(self):
        super().__init__()
        # 窗口基本设置
        self.title("记忆熔炉 v1.2")
        self.geometry("600x800")
        self.scheduler = SpacedRepetition()  # 初始化调度器
        self.deck = self.load_deck()  # 加载卡片数据
        self.current_card = None  # 当前显示的卡片

        # 初始化界面
        self.create_widgets()
        self.show_next_card()  # 显示第一个卡片
        # 设置关闭事件处理
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_widgets(self):
        """创建界面组件"""
        # 控制按钮面板
        control_frame = ttk.Frame(self)
        control_frame.pack(pady=10, fill="x")

        # 定义评分按钮配置
        buttons = [
            ("忘记 (0)", 0, "#FF6B6B"),  # 红色
            ("困难 (1)", 1, "#FFD93D"),  # 黄色
            ("一般 (2)", 2, "#6C5CE7"),  # 紫色
            ("记住 (3)", 3, "#00B894"),  # 绿色
        ]

        # 创建并排列评分按钮
        for text, q, color in buttons:
            btn = ttk.Button(
                control_frame,
                text=text,
                command=lambda q=q: self.rate_card(q),
                style=f"{color}.TButton",
            )
            btn.pack(side="left", padx=5, expand=True)

        # 卡片显示区域
        self.card_frame = ttk.Frame(self)
        self.card_frame.pack(pady=20, fill="both", expand=True)

        # 初始化统计图表
        self.figure = Figure(figsize=(5, 3), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # 配置按钮样式
        self.style = ttk.Style()
        self.style.configure("TButton", font=("微软雅黑", 10))
        # 为不同按钮设置颜色
        for color in ["#FF6B6B", "#FFD93D", "#6C5CE7", "#00B894"]:
            self.style.configure(
                f"{color}.TButton", foreground="white", background=color
            )

    def load_deck(self):
        """加载卡片数据"""
        # 默认卡片数据（当文件不存在时使用）
        default_cards = [
            {
                "front": "Python的GIL是指？",
                "back": "全局解释器锁 (Global Interpreter Lock)",
            },
            {"front": "@staticmethod的作用", "back": "声明静态方法，不需要实例参数"},
        ]

        try:
            # 尝试从JSON文件加载数据
            with open("flashcards.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                return [Card(**item) for item in data]
        except FileNotFoundError:
            # 文件不存在时使用默认卡片
            return [Card(**item) for item in default_cards]

    def save_deck(self):
        """保存卡片数据到JSON文件"""
        data = []
        for card in self.deck:
            data.append(
                {
                    "front": card.front,
                    "back": card.back,
                    "interval": card.interval,
                    "ease_factor": card.ease_factor,
                    "next_review": card.next_review.strftime("%Y-%m-%d %H:%M:%S"),
                    "review_count": card.review_count,
                    "history": card.history,
                }
            )

        # 写入JSON文件
        with open("flashcards.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def show_next_card(self):
        """显示下一个待复习的卡片"""
        # 清空当前卡片显示区域
        for widget in self.card_frame.winfo_children():
            widget.destroy()

        # 筛选需要复习的卡片（下次复习时间已到）
        due_cards = [c for c in self.deck if datetime.now() > c.next_review]
        if due_cards:
            self.current_card = due_cards[0]
            # 创建并显示卡片组件
            FlashCard(
                self.card_frame, self.current_card.front, self.current_card.back
            ).pack()
            self.update_chart()  # 更新统计图表
        else:
            self.update_chart()
            messagebox.showinfo("完成", "今日所有卡片已复习完成！")

    def rate_card(self, quality):
        """处理用户评分"""
        if self.current_card:
            self.scheduler.update_card(self.current_card, quality)
            self.show_next_card()

    def update_chart(self):
        """更新记忆曲线图表"""
        self.ax.clear()  # 清空旧图表

        # 收集所有卡片的历史数据
        dates = []
        intervals = []
        for card in self.deck:
            if card.history:
                # 获取最近一次复习日期
                last_date = datetime.strptime(card.history[-1][0], "%Y-%m-%d")
                dates.append(last_date)
                intervals.append(card.interval)

        # 绘制散点图
        if dates and intervals:
            self.ax.scatter(dates, intervals, c="#6C5CE7", alpha=0.7)
            self.ax.set_title("记忆间隔趋势")
            self.ax.set_ylabel("下次复习间隔（天）")
            self.ax.grid(True)
            self.figure.autofmt_xdate()  # 自动调整日期格式
            self.canvas.draw()  # 重绘画布

    def on_close(self):
        """处理窗口关闭事件"""
        self.save_deck()  # 保存数据
        self.destroy()


if __name__ == "__main__":
    app = FlashCardApp()
    app.mainloop()
