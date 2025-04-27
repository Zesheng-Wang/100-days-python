from tkinter import *
import requests
import html
from random import shuffle
from urllib.parse import unquote


def decode_api_data(data):
    """完整解码API返回数据"""
    return {
        "category": html.unescape(unquote(data["category"])),
        "question": html.unescape(unquote(data["question"])),
        "correct_answer": html.unescape(unquote(data["correct_answer"])),
        "incorrect_answers": [
            html.unescape(unquote(ans)) for ans in data["incorrect_answers"]
        ],
    }


def get_question():
    """获取天机题库问题"""
    params = {
        "amount": 1,
        "type": "multiple",  # 多选题
        "category": 18,  # 计算机类
        "encode": "url3986",  # 编码格式
    }

    try:
        response = requests.get("https://opentdb.com/api.php", params=params, timeout=5)
        data = response.json()
        data = data["results"][0]
        return decode_api_data(data)  # 使用解码函数
    except Exception as e:
        print(f"天机获取失败: {str(e)}")
        return None


class QuizApp:
    def __init__(self):
        self.window = Tk()
        self.window.title("天机问答")
        self.window.config(padx=20, pady=20, bg="#2C3E50")

        # 分数显示
        self.score = 0
        self.score_label = Label(
            text=f"修为：{self.score}",
            fg="white",
            bg="#2C3E50",
            font=("微软雅黑", 20, "bold"),
        )
        self.score_label.grid(row=0, column=1)

        # 问题画布
        self.canvas = Canvas(width=400, height=300, bg="#34495E", highlightthickness=0)
        self.question_text = self.canvas.create_text(
            200,
            150,
            text="天机加载中...",
            width=380,
            fill="white",
            font=("微软雅黑", 18),
        )
        self.canvas.grid(row=1, column=0, columnspan=2, pady=20)

        # 选项按钮
        self.buttons = []
        for i in range(4):
            btn = Button(
                text="",
                width=35,
                height=2,
                bg="#3498DB",
                fg="white",
                font=("微软雅黑", 12),
                command=lambda idx=i: self.check_answer(idx),
            )
            btn.grid(row=2 + i, column=0, columnspan=2, pady=5)
            self.buttons.append(btn)

        # 下一题按钮
        self.next_btn = Button(
            text="⟳ 下一题",
            command=self.next_question,
            state=DISABLED,
            bg="#27AE60",
            font=("微软雅黑", 14),
        )
        self.next_btn.grid(row=6, column=0, columnspan=2, pady=10)

        self.current_question = None
        self.next_question()  # 初始加载

        self.window.mainloop()

    def decode_text(self, text):
        """解码HTML特殊字符"""
        return html.unescape(text)

    def next_question(self):
        """加载新问题"""
        self.next_btn.config(state=DISABLED)
        question_data = get_question()

        if question_data:
            # 处理问题数据
            self.current_question = {
                "question": self.decode_text(question_data["question"]),
                "correct": self.decode_text(question_data["correct_answer"]),
                "options": [
                    self.decode_text(ans) for ans in question_data["incorrect_answers"]
                ]
                + [self.decode_text(question_data["correct_answer"])],
            }
            shuffle(self.current_question["options"])  # 随机选项顺序

            # 更新界面
            self.canvas.itemconfig(
                self.question_text, text=self.current_question["question"]
            )
            for i, btn in enumerate(self.buttons):
                btn.config(text=self.current_question["options"][i], bg="#3498DB")
        else:
            self.canvas.itemconfig(self.question_text, text="天机不可测，请稍后再试...")

    def check_answer(self, selected_idx):
        """验证答案"""
        selected = self.current_question["options"][selected_idx]
        correct = self.current_question["correct"]

        # 高亮显示结果
        for i, option in enumerate(self.current_question["options"]):
            if option == correct:
                self.buttons[i].config(bg="#27AE60")  # 正确答案绿色
            elif i == selected_idx:
                self.buttons[i].config(bg="#E74C3C")  # 错误答案红色

        # 更新分数
        if selected == correct:
            self.score += 10
            self.score_label.config(text=f"修为：{self.score}")

        self.next_btn.config(state=NORMAL)  # 启用下一题按钮


if __name__ == "__main__":
    QuizApp()
