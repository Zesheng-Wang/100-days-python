from pathlib import Path


def file_mover(target_dir: Path):
    """按扩展名自动分类文件到对应目录"""
    classification_rules = {
        "武学秘籍": ["pdf", "docx", "txt"],
        "灵丹妙药": ["jpg", "png", "gif"],
        "法宝图纸": ["py", "java", "cpp"],
        "天材地宝": ["zip", "rar", "7z"],
    }

    for file in target_dir.glob("*"):
        if file.is_file():
            # 提取扩展名并转换为小写
            extension = file.suffix[1:].lower()

            # 查找匹配的分类
            target_category = "杂物"  # 默认分类
            for category, suffix_list in classification_rules.items():
                if extension in suffix_list:
                    target_category = category
                    break

            # 创建分类目录并移动文件
            target_directory = target_dir / target_category
            target_directory.mkdir(exist_ok=True)
            file.rename(target_directory / file.name)
            print(f"【{file.name}】已移送至【{target_category}】")


if __name__ == "__main__":
    file_mover(Path(r"C:\乱七八糟"))
