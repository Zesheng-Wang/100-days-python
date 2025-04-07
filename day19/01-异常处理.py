import time

print(10 / 0)  # 这里会抛出 ZeroDivisionError

try:
    age = int(input("请输入年龄："))
    print(f"您今年{age}岁")
except ValueError:
    print("输入的不是数字！")


try:
    file = open("data.txt", "r")
    content = file.read()
    number = int(content)
except FileNotFoundError:
    print("文件不存在")
except ValueError:
    print("文件内容不是数字")
except Exception as e:
    print(f"发生未知错误：{e}")
finally:
    file.close()  # 无论是否出错都会执行


class InsufficientFundsError(Exception):
    """余额不足异常"""

    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount
        super().__init__(f"余额不足！当前余额：{balance}，需要：{amount}")


def withdraw(balance, amount):
    if amount > balance:
        raise InsufficientFundsError(balance, amount)
    return balance - amount


# 使用示例
try:
    withdraw(100, 200)
except InsufficientFundsError as e:
    print(e)
# 传统方式需要手动关闭
file = open("data.txt")
try:
    data = file.read()
finally:
    file.close()

# 现代方式（推荐）
with open("data.txt") as file:
    data = file.read()


# 离开with块后自动关闭文件
class Timer:
    """计时上下文管理器"""

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        self.end = time.time()
        print(f"耗时：{self.end - self.start:.2f}秒")


# 使用示例
with Timer():
    time.sleep(1.5)


import logging

logging.basicConfig(
    filename="error.log", level=logging.ERROR, format="%(asctime)s - %(message)s"
)

try:
    1 / 0
except Exception as e:
    logging.error("发生数学错误", exc_info=True)
