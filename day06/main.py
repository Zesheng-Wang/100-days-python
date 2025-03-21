import random

# ----------------------
# 常量定义
# ----------------------
WORD_LIST = ["PYTHON", "JAVA", "JAVASCRIPT", "RUBY", "HTML", "CSS"]
MAX_LIVES = 6  # 最大生命值

# ----------------------
# ASCII绞刑架图形（7个阶段）
# ----------------------
HANGMAN_STAGES = [
    """
       ------
       |    |
       O    |
      /|\   |
      / \   |
            |
    """,  # 生命值0（死亡）
    """
       ------
       |    |
       O    |
      /|\   |
      /     |
            |
    """,  # 生命值1
    """
       ------
       |    |
       O    |
      /|\   |
            |
            |
    """,  # 生命值2
    """
       ------
       |    |
       O    |
      /|    |
            |
            |
    """,  # 生命值3
    """
       ------
       |    |
       O    |
       |    |
            |
            |
    """,  # 生命值4
    """
       ------
       |    |
       O    |
            |
            |
            |
    """,  # 生命值5
    """
       ------
       |    |
            |
            |
            |
            |
    """,  # 生命值6（初始状态）
]


# ----------------------
# 函数定义
# ----------------------
def get_random_word() -> str:
    """从单词库随机获取一个单词"""
    return random.choice(WORD_LIST)


def display_hangman(lives: int):
    """显示绞刑架当前状态"""
    print(HANGMAN_STAGES[lives])


def display_progress(word: str, guessed_letters: set) -> str:
    """显示单词猜测进度（例如 P _ T _ O _）"""
    return " ".join([letter if letter in guessed_letters else "_" for letter in word])


def validate_input(char: str, guessed: set) -> bool:
    """验证玩家输入是否符合规则"""
    if len(char) != 1:
        print("请输入单个字母！")
        return False
    if not char.isalpha():
        print("请输入英文字母！")
        return False
    if char in guessed:
        print("这个字母已经猜过了！")
        return False
    return True


# ----------------------
# 游戏主逻辑
# ----------------------
def play_game():
    # 初始化游戏数据
    target_word = get_random_word()
    guessed_letters = set()
    incorrect_guesses = []
    lives = MAX_LIVES

    print("=== 欢迎来到Hangman猜词游戏 ===")
    print(f"单词长度：{len(target_word)}个字母")

    while lives > 0:
        # 显示当前状态
        print("\n" + "=" * 30)
        display_hangman(lives)
        print(f"已猜字母：{', '.join(incorrect_guesses)}")
        print("当前进度：", display_progress(target_word, guessed_letters))

        # 获取玩家输入
        guess = input("请输入一个字母：").upper()

        # 输入验证
        if not validate_input(guess, guessed_letters.union(incorrect_guesses)):
            continue

        # 处理猜测结果
        if guess in target_word:
            guessed_letters.add(guess)
            # 胜利条件判断
            if all(letter in guessed_letters for letter in target_word):
                print(f"\n恭喜！你猜对了！单词是：{target_word}")
                return
        else:
            incorrect_guesses.append(guess)
            lives -= 1

    # 失败处理
    print("\n" + "=" * 30)
    display_hangman(0)
    print(f"很遗憾，游戏结束！正确单词是：{target_word}")


# ----------------------
# 启动游戏
# ----------------------
if __name__ == "__main__":
    play_game()
