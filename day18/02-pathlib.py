from pathlib import Path

# 创建Path对象（自动适配操作系统）

current_dir = Path.cwd()
home_dir = Path.home()  # 用户主目录
# 路径拼接（使用/运算符）
log_file = current_dir / "logs" / "app.log"
# 文件属性检测
print(f"是否存在：{log_file.exists()}")
print(f"是文件吗：{log_file.is_file()}")
print(f"文件大小：{log_file.stat().st_size}字节")
