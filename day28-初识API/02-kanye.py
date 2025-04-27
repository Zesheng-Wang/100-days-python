from tkinter import *            # 导入 Tkinter GUI 库中的所有组件
import requests                 # 导入用于发送 HTTP 请求的 requests 库

def get_quote():
    """获取 Kanye 随机语录并更新画布文本"""
    response = requests.get("https://api.kanye.rest")   # 向 Kanye.rest API 发送 GET 请求
    response.raise_for_status()                         # 如果响应状态不是 200，会抛出异常
    data = response.json()                              # 将响应内容解析为 JSON 字典
    quote = data["quote"]                               # 从字典中提取 "quote" 字段
    canvas.itemconfig(quote_text, text=quote)           # 更新画布上 quote_text 对象的文本内容

# —— 创建主窗口 ——
window = Tk()                                          # 创建 Tkinter 应用主窗口实例
window.title("Kanye 天机语")                           # 设置窗口标题
window.config(padx=50, pady=50)                        # 设置窗口内边距，左右上下各留白 50 像素

# —— 配置画布与背景 ——
canvas = Canvas(width=300, height=414)                 # 创建画布，宽 300、高 414 像素
background_img = PhotoImage(file="background.png")      # 加载背景图片，文件名须与脚本同目录
canvas.create_image(150, 207, image=background_img)     # 在画布中心(150,207)绘制背景图片
quote_text = canvas.create_text(
    150, 207,                                          # 文本位置：画布中心
    text="Kanye Quote Goes HERE",                      # 初始显示的占位文本
    width=250,                                         # 文本框宽度，超出自动换行
    font=("Arial", 30, "bold"),                        # 字体：Arial，字号 30，加粗
    fill="white"                                       # 文本颜色：白色
)
canvas.grid(row=0, column=0)                           # 使用 grid 布局，将画布放置在第 0 行第 0 列

# —— 配置按钮 ——
kanye_img = PhotoImage(file="kanye.png")               # 加载按钮图标图片
kanye_button = Button(
    image=kanye_img,                                   # 将按钮显示为图片
    highlightthickness=0,                              # 去除按钮点击时的高亮边框
    command=get_quote                                   # 单击按钮时调用 get_quote 函数
)
kanye_button.grid(row=1, column=0)                     # 将按钮放置在第 1 行第 0 列

# —— 进入 Tkinter 主事件循环 ——
window.mainloop()                                      # 启动事件循环，保持窗口运行并响应用户操作
