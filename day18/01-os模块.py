import os

# 获取当前工作目录（相当于Linux的pwd）
current_path = os.getcwd()
print(f"当前修炼洞府：{current_path}")

# 列出目录内容（相当于ls命令）
file_list = os.listdir(".")
print("目录藏宝图：", file_list)

# 递归遍历目录（深度优先搜索）
for root, dirs, files in os.walk("../"):
    print(f"\n发现秘境：{root}")
    print("内有洞天：", dirs)
    print("藏经阁秘籍：", files)

import os

# 示例路径
example_path = "/home/user/docs/file.txt"

# 1. 拼接路径 - 自动处理不同操作系统的路径分隔符
new_path = os.path.join("dir1", "dir2", "file.txt")
print(new_path)  # 输出: dir1/dir2/file.txt (Linux/macOS) 或 dir1\dir2\file.txt (Windows)

# 2. 获取绝对路径
abs_path = os.path.abspath("relative/path")
print(abs_path)  # 输出当前工作目录下relative/path的绝对路径

# 3. 获取路径的目录部分（去掉文件名）
dir_name = os.path.dirname(example_path)
print(dir_name)  # 输出: /home/user/docs

# 4. 获取路径的文件名部分（最后一个组成部分）
file_name = os.path.basename(example_path)
print(file_name)  # 输出: file.txt

# 5. 分割路径为目录和文件名两部分
dir_part, file_part = os.path.split(example_path)
print(dir_part, file_part)  # 输出: ('/home/user/docs', 'file.txt')

# 6. 分割文件扩展名
file_name, ext = os.path.splitext(file_part)
print(file_name, ext)  # 输出: ('file', '.txt')

# 7. 检查路径是否存在
exists = os.path.exists(example_path)
print(f"路径存在: {exists}")

# 8. 检查是否是目录
is_dir = os.path.isdir("/home/user/docs")
print(f"是目录: {is_dir}")

# 9. 检查是否是文件
is_file = os.path.isfile(example_path)
print(f"是文件: {is_file}")

# 10. 创建目录（递归创建）
os.makedirs("new/directory/path", exist_ok=True)  # exist_ok=True表示目录存在时不报错

# 11. 获取当前工作目录
cwd = os.getcwd()
print(f"当前工作目录: {cwd}")

# 12. 路径标准化（处理多余的斜杠和..）
norm_path = os.path.normpath("/home//user/../docs/file.txt")
print(norm_path)  # 输出: /home/docs/file.txt
