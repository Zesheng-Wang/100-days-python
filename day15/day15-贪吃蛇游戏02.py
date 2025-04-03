# 导入必要的库
import arcade  # 游戏开发库
import random  # 随机数生成
from typing import List  # 类型提示支持

# ----------------------
# 基础类定义
# ----------------------
class Vector2:
    """二维坐标类"""
    def __init__(self, x: int, y: int):
        self.x = x  # x坐标
        self.y = y  # y坐标

    def __add__(self, other):
        """向量加法"""
        return Vector2(self.x + other.x, self.y + other.y)
    
    def __eq__(self, other):
        """等值比较"""
        return self.x == other.x and self.y == other.y
    
    def __mod__(self, value):
        """用于实现循环边界（取模运算）"""
        return Vector2(self.x % value, self.y % value)

# 方向常量字典（使用Vector2表示方向向量）
DIRECTIONS = {
    "up": Vector2(0, 1),     # 上
    "down": Vector2(0, -1),  # 下
    "left": Vector2(-1, 0),  # 左
    "right": Vector2(1, 0)    # 右
}

# ----------------------
# 蛇类继承体系
# ----------------------
class BaseSnake:
    """蛇基类（所有蛇类的共同行为）"""
    def __init__(self, start_pos: Vector2):
        self.body: List[Vector2] = [start_pos]  # 身体坐标列表
        self.direction: Vector2 = DIRECTIONS["right"]  # 初始方向向右
        self.grow_counter = 0  # 生长计数器（记录需要生长的节数）
    
    def move(self):
        """基础移动逻辑（所有蛇类共用）"""
        new_head = self.body[-1] + self.direction  # 计算新头部位置
        self.body.append(new_head)  # 将新头部添加到身体
        
        # 根据生长计数器判断是否缩短尾部
        if self.grow_counter > 0:
            self.grow_counter -= 1
        else:
            self.body.pop(0)  # 移除尾部保持长度
    
    def check_collision(self, grid_size: int) -> bool:
        """碰撞检测（子类可重写）返回是否碰撞自身"""
        head = self.body[-1]  # 获取头部位置
        return head in self.body[:-1]  # 检查头部是否在身体其他部分
    
    def grow(self, amount: int = 1):
        """生长机制（延长蛇身）"""
        self.grow_counter += amount  # 增加生长计数器

class TeleportSnake(BaseSnake):
    """瞬移蛇（穿越边界实现循环地图）"""
    def move(self):
        """重写移动方法实现边界穿越"""
        super().move()  # 先执行基础移动
        head = self.body[-1]  # 获取移动后的头部
        self.body[-1] = head % 20  # 对坐标取模实现循环边界（假设20x20网格）

class SplitSnake(BaseSnake):
    """分身蛇（可分裂身体）"""
    def __init__(self, start_pos: Vector2):
        super().__init__(start_pos)
        self.children: List[List[Vector2]] = []  # 存储所有分身身体的列表
    
    def split(self):
        """分裂身体创建分身"""
        if len(self.body) >= 4:  # 至少4节才能分裂
            split_point = len(self.body) // 2  # 计算分裂点（取中间）
            new_body = self.body[split_point:]  # 后半部分作为分身
            self.body = self.body[:split_point]  # 保留前半部分作为本体
            self.children.append(new_body)  # 将分身添加到列表
    
    def update_children(self):
        """更新所有分身的位置（模拟移动）"""
        for child in self.children:
            if len(child) > 1:
                child.pop(0)  # 移除分身尾部实现移动效果

# ----------------------
# 游戏主类
# ----------------------
class AdvancedSnakeGame(arcade.Window):
    """游戏主窗口类（继承arcade.Window）"""
    def __init__(self):
        # 初始化窗口（800x600像素，标题为"灵蛇进化录"）
        super().__init__(800, 600, "灵蛇进化录")
        self.grid_size = 20  # 网格尺寸（20x20）
        self.cell_size = 30  # 每个网格的像素大小
        self.snake: BaseSnake = TeleportSnake(Vector2(10, 10))  # 创建瞬移蛇实例（初始位置中心）
        self.food = self.generate_food()  # 生成食物
        self.score = 0  # 玩家得分
        self.game_over = False  # 游戏结束标志
        
        # 移动时间控制相关
        self.move_interval = 0.15  # 移动间隔（秒）
        self.time_since_move = 0.0  # 累计时间
        
        arcade.set_background_color(arcade.color.BLACK)  # 设置背景颜色

    def generate_food(self) -> Vector2:
        """生成不在蛇身上的随机食物位置"""
        while True:
            # 随机生成坐标（0到19之间）
            pos = Vector2(random.randint(0,19), random.randint(0,19))
            if pos not in self.snake.body:  # 确保食物不在蛇身上
                return pos

    def on_draw(self):
        """绘制游戏画面（每帧自动调用）"""
        self.clear()  # 清空画面
        
        # 绘制食物（红色圆形）
        arcade.draw_circle_filled(
            self.food.x * self.cell_size + self.cell_size//2,  # 计算x屏幕坐标
            self.food.y * self.cell_size + self.cell_size//2,  # 计算y屏幕坐标
            self.cell_size//2 - 2,  # 半径（留2像素边距）
            arcade.color.RED  # 颜色
        )
        
        # 绘制主蛇身体（交替颜色实现流光效果）
        for i, seg in enumerate(self.snake.body):
            # 交替使用两种绿色
            color = arcade.color.GREEN if i%2==0 else arcade.color.LIME_GREEN
            # 绘制矩形代表蛇身节
            arcade.draw_rect_filled(
                # 创建矩形参数（XYWH格式）
                arcade.rect.XYWH(
                    seg.x * self.cell_size + 1,  # 计算x位置（留1像素边距）
                    seg.y * self.cell_size + 1,  # 计算y位置
                    self.cell_size - 2,  # 宽度
                    self.cell_size - 2  # 高度
                ),
                color  # 填充颜色
            )
        
        # 如果使用分身蛇，绘制分身身体
        if isinstance(self.snake, SplitSnake):
            for child in self.snake.children:  # 遍历所有分身
                # 只绘制最后3节（-3表示倒数第三个元素开始）
                for seg in child[-3:]:
                    # 类似主蛇绘制，可以调整颜色参数
                    arcade.draw_rect_filled(...)  # 实际代码需要完整参数
        
        # 在左上角绘制分数（白色文字）
        arcade.draw_text(
            f"修为: {self.score}",  # 显示分数
            10, self.height-40,  # 坐标（10, 560）
            arcade.color.WHITE, 20  # 颜色和字号
        )

    def on_update(self, delta_time: float):
        """游戏状态更新（每帧调用）"""
        if self.game_over:
            return  # 游戏结束停止更新
        
        self.time_since_move += delta_time  # 累计时间
        # 达到移动间隔时执行移动
        if self.time_since_move >= self.move_interval:
            self.time_since_move = 0  # 重置计时器
            self.snake.move()  # 移动蛇
            
            # 检测是否吃到食物
            if self.snake.body[-1] == self.food:
                self.score += 1  # 增加分数
                self.snake.grow(3)  # 生长3节
                self.food = self.generate_food()  # 生成新食物
            
            # 检测碰撞（调用蛇类的碰撞检测方法）
            if self.snake.check_collision(self.grid_size):
                self.game_over = True  # 触发游戏结束

    def on_key_press(self, key: int, modifiers: int):
        """键盘按下事件处理"""
        if self.game_over:
            return  # 游戏结束不响应
        
        # 方向键控制（防止180度转向）
        if key == arcade.key.UP and self.snake.direction != DIRECTIONS["down"]:
            self.snake.direction = DIRECTIONS["up"]
        elif key == arcade.key.DOWN and self.snake.direction != DIRECTIONS["up"]:
            self.snake.direction = DIRECTIONS["down"]
        elif key == arcade.key.LEFT and self.snake.direction != DIRECTIONS["right"]:
            self.snake.direction = DIRECTIONS["left"]
        elif key == arcade.key.RIGHT and self.snake.direction != DIRECTIONS["left"]:
            self.snake.direction = DIRECTIONS["right"]
        
        # 空格键触发分身分裂（仅SplitSnake有效）
        if key == arcade.key.SPACE and isinstance(self.snake, SplitSnake):
            self.snake.split()  # 调用分裂方法

# 程序入口
if __name__ == "__main__":
    game = AdvancedSnakeGame()  # 创建游戏实例
    arcade.run()  # 运行游戏循环