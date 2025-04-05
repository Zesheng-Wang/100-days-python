import turtle  # 导入turtle模块，用于绘制游戏界面
import random  # 导入random模块，用于生成随机数
import time  # 导入time模块，用于控制游戏帧率

# ====================
#   游戏初始化设置
# ====================
win = turtle.Screen()  # 创建游戏窗口
win.setup(width=600, height=600)  # 设置窗口大小
win.bgcolor("lightgray")  # 设置窗口背景颜色为浅灰色
win.title("龟仙人の马路大冒险")  # 设置窗口标题
win.tracer(0)  # 关闭自动刷新，提高性能，需要手动调用win.update()刷新屏幕

# ====================
#     玩家角色
# ====================
player = turtle.Turtle()  # 创建玩家角色
player.shape("turtle")  # 设置形状为乌龟
player.color("darkgreen")  # 设置颜色为深绿色
player.penup()  # 关闭画笔，防止乌龟移动时画出轨迹
player.setheading(90)  # 设置乌龟朝向上方（90度）
player.goto(0, -250)  # 将玩家初始化位置放在底部中央

# ====================
#     计分系统
# ====================
score = 0  # 初始化得分为0
score_display = turtle.Turtle()  # 创建用于显示分数的乌龟对象
score_display.hideturtle()  # 隐藏乌龟形状
score_display.penup()  # 关闭画笔
score_display.goto(-280, 260)  # 设置分数显示位置（屏幕左上角）
score_display.write(f"得分: {score}", font=("Arial", 14, "normal"))  # 绘制分数文本

# ====================
#     障碍物系统
# ====================
car_list = []  # 用于存储所有障碍物的小车
colors = ["red", "blue", "orange", "purple", "brown"]  # 定义障碍物颜色列表


def create_car():
    """生成新的障碍物（小车）"""
    car = turtle.Turtle()  # 创建新的乌龟对象作为小车
    car.shape("square")  # 设置形状为方块
    car.shapesize(1, 2)  # 调整大小，使其变成长方形（1格高，2格宽）
    car.color(random.choice(colors))  # 随机设置小车颜色
    car.penup()  # 关闭画笔
    car.speed(0)  # 设置小车绘制速度为最快

    # 随机生成小车起始Y坐标，范围在-200到200之间
    start_y = random.randint(-200, 200)
    # 计算小车的速度，基础速度2-5，并随着得分增加提高难度
    speed = random.randint(2, 5) + score // 2
    car.goto(300, start_y)  # 将小车放置在右侧屏幕外（x=300）
    car.speed = -speed  # 设置小车的移动速度，向左移动

    car_list.append(car)  # 将新生成的小车加入到列表中


# 初始生成5个障碍物
for _ in range(5):
    create_car()


# ====================
#     玩家控制
# ====================
def move_up():
    """玩家向上移动"""
    y = player.ycor()  # 获取当前玩家的Y坐标
    if y < 250:  # 限制玩家不能超出屏幕顶部
        player.sety(y + 20)  # 向上移动20个像素
    check_success()  # 检测是否成功到达终点


win.listen()  # 监听键盘输入
win.onkeypress(move_up, "Up")  # 当按下“↑”键时，调用move_up函数


# ====================
#     游戏逻辑
# ====================
def check_collision():
    """检测玩家是否撞到障碍物"""
    for car in car_list:
        if player.distance(car) < 25:  # 如果玩家与小车的距离小于25，则判定为碰撞
            return True
    return False


def check_success():
    """检测玩家是否成功穿越马路"""
    global score
    if player.ycor() >= 250:  # 如果玩家到达屏幕顶部
        score += 10  # 增加得分
        score_display.clear()  # 清空旧的分数
        score_display.write(f"得分: {score}", font=("Arial", 14, "normal"))  # 更新分数
        player.goto(0, -250)  # 将玩家重置到起点


def game_over():
    """游戏结束处理"""
    global game_running
    game_running = False  # 设置游戏状态为停止
    over = turtle.Turtle()  # 创建游戏结束提示文本的乌龟对象
    over.hideturtle()  # 隐藏乌龟
    over.write("GAME OVER!", align="center", font=("Arial", 24, "bold"))  # 显示"GAME OVER!"


# ====================
#     主游戏循环
# ====================
game_running = True  # 游戏运行状态
last_car_time = time.time()  # 记录上一次生成障碍物的时间

while game_running:
    win.update()  # 刷新屏幕

    # 移动所有障碍物
    for car in car_list:
        car.setx(car.xcor() + car.speed)  # 让小车向左移动

        # 当小车超出左边界时，移除并生成新小车
        if car.xcor() < -320:
            car.hideturtle()  # 隐藏小车
            car_list.remove(car)  # 从列表中移除
            create_car()  # 生成新的小车

    # 每隔2秒生成一个新的小车
    if time.time() - last_car_time > 2:
        create_car()
        last_car_time = time.time()  # 更新最后一次生成时间

    # 检测玩家是否撞到障碍物
    if check_collision():
        game_over()

    time.sleep(0.016)  # 约60帧每秒（1秒 / 60 ≈ 0.016）

win.mainloop()  # 进入turtle事件循环
