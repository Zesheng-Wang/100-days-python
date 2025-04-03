import arcade  # 导入 arcade 库，用于图形渲染和游戏开发
import random  # 导入 random 库，用于生成随机数

# 定义一个二维向量类，用于表示位置和方向
class Vector2:
    def __init__(self, x, y):
        self.x = x  # x 坐标
        self.y = y  # y 坐标

    # 定义向量加法运算，使得可以直接相加两个 Vector2 对象
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    # 定义等于运算，使得可以比较两个 Vector2 是否相等
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

# 方向字典，存储上下左右移动的单位向量
DIRECTIONS = {
    "up": Vector2(0, 1),     # 向上移动
    "down": Vector2(0, -1),  # 向下移动
    "left": Vector2(-1, 0),  # 向左移动
    "right": Vector2(1, 0),  # 向右移动
}

# 游戏状态类，存储蛇的位置、方向、食物等信息
class GameState:
    def __init__(self, width=20, height=20):
        self.snake = [Vector2(5, 5)]  # 初始化蛇的位置，初始长度为 1
        self.direction = DIRECTIONS["right"]  # 初始方向向右
        self.food = self._generate_food()  # 生成食物
        self.score = 0  # 分数
        self.game_over = False  # 游戏是否结束的标志

    # 生成食物，确保食物不会出现在蛇身上
    def _generate_food(self):
        while True:
            new_food = Vector2(random.randint(0, 19), random.randint(0, 19))  # 在 0-19 范围内随机生成食物位置
            if new_food not in self.snake:  # 确保食物不会出现在蛇身上
                return new_food

# 贪吃蛇游戏窗口类，继承自 arcade.Window
class SnakeGame(arcade.Window):
    def __init__(self):
        super().__init__(width=400, height=400, title="贪吃蛇修仙版")  # 设置窗口大小和标题
        self.cell_size = 20  # 每个格子的大小
        self.game = GameState()  # 创建游戏状态对象
        arcade.set_background_color(arcade.color.BLACK)  # 设置背景颜色为黑色
        
        # 控制蛇的移动速度（单位：秒）
        self.move_interval = 0.2  # 每 0.2 秒移动一次
        self.time_since_last_move = 0.0  # 记录距离上次移动的时间

    # 绘制游戏内容
    def on_draw(self):
        self.clear()  # 清除屏幕

        # 绘制蛇的每个身体部分
        for segment in self.game.snake:
            arcade.draw_rect_filled(
                arcade.rect.XYWH(
                    segment.x * self.cell_size + 1,  # 计算绘制的 x 坐标
                    segment.y * self.cell_size + 1,  # 计算绘制的 y 坐标
                    self.cell_size - 2,  # 宽度
                    self.cell_size - 2   # 高度
                ),
                arcade.color.GREEN  # 设置蛇的颜色为绿色
            )

        # 绘制食物
        arcade.draw_circle_filled(
            self.game.food.x * self.cell_size + self.cell_size // 2,  # 计算食物的 x 坐标
            self.game.food.y * self.cell_size + self.cell_size // 2,  # 计算食物的 y 坐标
            self.cell_size // 2 - 2,  # 计算食物的半径
            arcade.color.RED  # 设置食物的颜色为红色
        )

        # 显示分数
        arcade.draw_text(
            f"修为: {self.game.score}",  # 文字内容
            10, self.height - 30,  # 文字位置（左上角）
            arcade.color.WHITE,  # 文字颜色
            16  # 文字大小
        )

    # 游戏逻辑更新，每帧调用一次
    def on_update(self, delta_time):
        if not self.game.game_over:  # 只有在游戏未结束时才更新
            self.time_since_last_move += delta_time  # 累积时间
            
            # 只有当累计时间超过移动间隔时才进行移动
            if self.time_since_last_move >= self.move_interval:
                self.time_since_last_move = 0.0  # 重置计时器
                self._move_snake()  # 移动蛇
                self._check_collisions()  # 检查碰撞

    # 移动蛇
    def _move_snake(self):
        new_head = self.game.snake[-1] + self.game.direction  # 计算新的蛇头位置
        self.game.snake.append(new_head)  # 将新的头部添加到蛇身

        if new_head == self.game.food:  # 如果蛇吃到了食物
            self.game.score += 1  # 分数加 1
            self.game.food = self.game._generate_food()  # 生成新的食物
        else:
            self.game.snake.pop(0)  # 如果没有吃到食物，则移除蛇尾（保持长度）

    # 检查蛇是否撞墙或咬到自己
    def _check_collisions(self):
        head = self.game.snake[-1]  # 获取蛇头位置
        if not (0 <= head.x < 20 and 0 <= head.y < 20):  # 检查是否超出边界
            self.game.game_over = True  # 结束游戏
        if head in self.game.snake[:-1]:  # 检查是否咬到自己
            self.game.game_over = True  # 结束游戏

    # 处理键盘输入
    def on_key_press(self, key, modifiers):
        # 上方向键，防止直接反向
        if key == arcade.key.UP and self.game.direction != DIRECTIONS["down"]:
            self.game.direction = DIRECTIONS["up"]
        # 下方向键，防止直接反向
        elif key == arcade.key.DOWN and self.game.direction != DIRECTIONS["up"]:
            self.game.direction = DIRECTIONS["down"]
        # 左方向键，防止直接反向
        elif key == arcade.key.LEFT and self.game.direction != DIRECTIONS["right"]:
            self.game.direction = DIRECTIONS["left"]
        # 右方向键，防止直接反向
        elif key == arcade.key.RIGHT and self.game.direction != DIRECTIONS["left"]:
            self.game.direction = DIRECTIONS["right"]

# 运行游戏
if __name__ == "__main__":
    game = SnakeGame()  # 创建游戏窗口
    arcade.run()  # 运行游戏
