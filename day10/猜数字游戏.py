import random

def create_game(difficulty='normal'):
    """创建猜数字游戏闭包"""
    # 根据难度设置范围
    ranges = {
        'easy': (1, 50),
        'normal': (1, 100),
        'hard': (1, 200)
    }
    min_num, max_num = ranges[difficulty]

    secret = random.randint(min_num, max_num)
    attempts = 0

    def guess(number):
        """猜测数字并返回结果"""
        nonlocal attempts  # 使用外层作用域的attempts

        attempts += 1

        if number < secret:
            return "太小了！", False
        elif number > secret:
            return "太大了！", False
        else:
            return f"恭喜！用了{attempts}次猜中！", True

    def get_hint():
        """获得提示（闭包访问secret）"""
        return f"提示：数字在{min_num}-{max_num}之间"

    return guess, get_hint

# --------------------------
# 游戏主程序
# --------------------------
if __name__ == "__main__":
    print("=== 数字猜谜修仙版 ===")

    # 初始化游戏
    difficulty = input("选择难度（easy/normal/hard）：")
    guess_func, hint_func = create_game(difficulty)
    print(hint_func())

    # 游戏循环
    while True:
        try:
            user_guess = int(input("输入你的猜测："))
            result, success = guess_func(user_guess)
            print(result)

            if success:
                break
        except ValueError:
            print("请输入有效数字！")
