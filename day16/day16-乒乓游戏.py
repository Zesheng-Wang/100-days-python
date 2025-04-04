import arcade  # 导入 arcade 游戏框架
import random  # 导入 random 模块，用于生成随机数

# ----------------------
# 常量定义
# ----------------------
SCREEN_WIDTH = 800  # 游戏窗口宽度
SCREEN_HEIGHT = 600  # 游戏窗口高度
PADDLE_COLORS = [arcade.color.BLUE, arcade.color.RED]  # 左右球拍颜色


class Vector2:
    """二维向量类（用于表示位置和速度）"""

    def __init__(self, x, y):
        self.x = x  # X 坐标或速度
        self.y = y  # Y 坐标或速度

    def __add__(self, other):
        # 向量加法
        return Vector2(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar):
        # 向量乘以标量
        return Vector2(self.x * scalar, self.y * scalar)


class Paddle:
    """球拍类"""

    def __init__(self, side: str):
        self.side = side  # 表示是左边还是右边球拍（'left' 或 'right'）
        self.width = 15  # 球拍宽度
        self.height = 80  # 球拍高度
        self.speed = 8  # 球拍移动速度
        self.score = 0  # 当前得分
        # 初始化球拍位置（左边在 x=50，右边在 x=750）
        self.pos = Vector2(50 if side == "left" else 750, 300)


class Ball:
    """球类"""

    def __init__(self):
        self.radius = 10  # 球的半径
        self.reset()  # 初始化位置和速度
        self.trail = []  # 用于记录球的移动轨迹，产生尾迹效果

    def reset(self):
        """重置球的位置和速度"""
        self.pos = Vector2(400, 300)  # 回到中心
        self.vel = Vector2(5, random.choice([-4, 4]))  # 设置初始速度


# ----------------------
# 游戏主类
# ----------------------
class PongGame(arcade.Window):
    def __init__(self):
        # 初始化窗口
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "乒乓修仙传")
        self.left_paddle = Paddle("left")  # 创建左球拍
        self.right_paddle = Paddle("right")  # 创建右球拍
        self.ball = Ball()  # 创建球对象
        self.game_active = False  # 游戏是否处于进行中状态

        self.keys_pressed = set()  # 保存当前按下的按键
        arcade.set_background_color(arcade.color.DARK_GREEN)  # 设置背景色

    def on_draw(self):
        self.clear()  # 清屏

        # 画中间的分割线
        arcade.draw_line(
            SCREEN_WIDTH / 2, 0, SCREEN_WIDTH / 2, SCREEN_HEIGHT, arcade.color.WHITE, 2
        )

        # 绘制两个球拍
        for paddle, color in zip([self.left_paddle, self.right_paddle], PADDLE_COLORS):
            arcade.draw_rect_filled(
                arcade.rect.XYWH(
                    paddle.pos.x, paddle.pos.y, paddle.width, paddle.height
                ),
                color,
            )

        # 绘制球的尾迹
        for i, pos in enumerate(self.ball.trail):
            alpha = 255 * (1 - i / len(self.ball.trail))  # 越靠前越透明
            arcade.draw_circle_filled(
                pos.x, pos.y, self.ball.radius, (255, 255, 255, int(alpha))
            )

        # 绘制球体
        arcade.draw_circle_filled(
            self.ball.pos.x, self.ball.pos.y, self.ball.radius, arcade.color.WHITE
        )

        # 显示比分
        self._draw_score()

    def _draw_score(self):
        # 显示左边比分
        arcade.draw_text(
            f"{self.left_paddle.score}",
            SCREEN_WIDTH / 2 - 60,
            550,
            arcade.color.WHITE,
            40,
            align="center",
            anchor_x="center",
        )
        # 显示右边比分
        arcade.draw_text(
            f"{self.right_paddle.score}",
            SCREEN_WIDTH / 2 + 60,
            550,
            arcade.color.WHITE,
            40,
            align="center",
            anchor_x="center",
        )

    def on_update(self, delta_time):
        if not self.game_active:
            return  # 如果游戏未开始，则不更新

        self._move_paddles()  # 处理球拍移动

        self.ball.pos += self.ball.vel  # 更新球的位置

        # 更新尾迹（只保留最近 5 个位置）
        self.ball.trail.append(Vector2(self.ball.pos.x, self.ball.pos.y))
        if len(self.ball.trail) > 5:
            self.ball.trail.pop(0)

        self._check_wall_collision()  # 检查上下边界碰撞
        self._check_paddle_collision()  # 检查与球拍碰撞
        self._check_score()  # 检查是否得分

    def _move_paddles(self):
        """根据按键移动球拍"""

        # 左球拍控制（W 和 S）
        if arcade.key.W in self.keys_pressed:
            self.left_paddle.pos.y = min(
                SCREEN_HEIGHT - self.left_paddle.height / 2,
                self.left_paddle.pos.y + self.left_paddle.speed,
            )
        if arcade.key.S in self.keys_pressed:
            self.left_paddle.pos.y = max(
                self.left_paddle.height / 2,
                self.left_paddle.pos.y - self.left_paddle.speed,
            )

        # 右球拍控制（方向键 ↑ 和 ↓）
        if arcade.key.UP in self.keys_pressed:
            self.right_paddle.pos.y = min(
                SCREEN_HEIGHT - self.right_paddle.height / 2,
                self.right_paddle.pos.y + self.right_paddle.speed,
            )
        if arcade.key.DOWN in self.keys_pressed:
            self.right_paddle.pos.y = max(
                self.right_paddle.height / 2,
                self.right_paddle.pos.y - self.right_paddle.speed,
            )

    def _check_wall_collision(self):
        """检测上下边界碰撞，撞到后反弹"""
        if (
            self.ball.pos.y < self.ball.radius
            or self.ball.pos.y > SCREEN_HEIGHT - self.ball.radius
        ):
            self.ball.vel.y *= -1  # Y方向反弹

    def _check_paddle_collision(self):
        """检测球与球拍是否碰撞"""
        for paddle in [self.left_paddle, self.right_paddle]:
            if abs(self.ball.pos.x - paddle.pos.x) < (
                paddle.width / 2 + self.ball.radius
            ) and abs(self.ball.pos.y - paddle.pos.y) < (
                paddle.height / 2 + self.ball.radius
            ):
                # 计算偏移量（用来控制弹射方向）
                offset = (self.ball.pos.y - paddle.pos.y) / (paddle.height / 2)
                self.ball.vel.x *= -1.1  # 反弹并加速
                self.ball.vel.y = offset * 8  # 根据偏移决定Y速度

                # 限制最大速度
                self.ball.vel = Vector2(
                    max(-10, min(10, self.ball.vel.x)),
                    max(-8, min(8, self.ball.vel.y)),
                )

    def _check_score(self):
        """检查球是否飞出边界，判断得分"""
        if self.ball.pos.x < 0:
            self.right_paddle.score += 1  # 右边得分
            self._reset_round()  # 重置回合
        elif self.ball.pos.x > SCREEN_WIDTH:
            self.left_paddle.score += 1  # 左边得分
            self._reset_round()

    def _reset_round(self):
        """重置球的位置，暂停游戏"""
        self.ball.reset()
        self.game_active = False

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)  # 添加按下的键到集合
        if key == arcade.key.SPACE and not self.game_active:
            self.game_active = True  # 按空格开始游戏

    def on_key_release(self, key, modifiers):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)  # 松开按键时从集合中移除


# 程序入口
if __name__ == "__main__":
    game = PongGame()  # 创建游戏窗口
    arcade.run()  # 启动游戏主循环
