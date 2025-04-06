import shutil

# 1. 复制文件 (保留权限，不保留元数据)
shutil.copy("src.txt", "dst.txt")  # 类似 cp src.txt dst.txt

# 2. 复制文件 (保留元数据，如修改时间)
shutil.copy2("src.txt", "dst.txt")  # 比 copy 更完整

# 3. 递归复制整个目录树
shutil.copytree("src_dir", "dst_dir")  # 类似 cp -r src_dir dst_dir

# 4. 递归删除目录树（慎用！不可逆操作）
shutil.rmtree("dir_to_delete")  # 类似 rm -rf dir_to_delete

# 5. 移动文件/目录（可跨磁盘）
shutil.move("old_path", "new_path")  # 类似 mv old_path new_path


# 1. 大文件流式复制（避免内存溢出）
with open("src.iso", "rb") as src, open("dst.iso", "wb") as dst:
    shutil.copyfileobj(src, dst, length=16*1024)  # 16KB 缓冲区

# 2. 保留文件权限（类似 chmod）
shutil.copymode("src.txt", "dst.txt")  # 仅复制权限
shutil.copystat("src.txt", "dst.txt")  # 复制权限和元数据

# 3. 处理同名目录（自动覆盖）
shutil.rmtree("dst_dir", ignore_errors=True)  # 先删除旧目录
shutil.copytree("src_dir", "dst_dir")        # 再复制新目录