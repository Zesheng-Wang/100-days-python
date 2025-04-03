class GameState:
    def __init__(self, width=20, height=20):
        self.snake = [Vector2(5, 5)]  # 蛇身坐标列表
        self.direction = DIRECTIONS["right"]
        self.food = self._generate_food()
        self.score = 0
        self.game_over = False

    def _generate_food(self):
        """在随机位置生成食物（不与蛇身重叠）"""
        while True:
            new_food = Vector2(
                random.randint(0, 19),
                random.randint(0, 19)
            )
            if new_food not in self.snake:
                return new_food
