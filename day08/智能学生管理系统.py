# --------------------------

# 系统初始化数据

# --------------------------

classes = [
    {  # 班级1
        "name": "筑基一班",
        "students": [
            {
                "id": 1001,
                "name": "韩立",
                "scores": {"炼丹术": 92, "御剑术": 88, "阵法": 95},
            },
            {
                "id": 1002,
                "name": "南宫婉",
                "scores": {"炼丹术": 95, "御剑术": 91, "阵法": 89},
            },
        ],
    },
    {  # 班级2
        "name": "金丹二班",
        "students": [
            {
                "id": 2001,
                "name": "厉飞雨",
                "scores": {"炼丹术": 85, "御剑术": 93, "阵法": 82},
            }
        ],
    },
]

# --------------------------

# 核心功能函数

# --------------------------


def add_student(class_index, student_data):
    """添加学生到指定班级"""

    classes[class_index]["students"].append(student_data)


def find_student(student_id):
    """通过ID查找学生（返回第一个匹配项）"""

    return next(
        (s for c in classes for s in c["students"] if s["id"] == student_id), None
    )


def analyze_scores():
    """全年级成绩分析"""

    # 使用lambda计算各科平均分

    subjects = ["炼丹术", "御剑术", "阵法"]
    total_students = sum(1 for c in classes for s in c["students"])
    averages = {
        sub: round(sum(
            s["scores"][sub]
            for c in classes
            for s in c["students"]
        ) / total_students, 1)
        for sub in subjects
    }

    # 使用lambda筛选优秀学生（平均分≥90）

    top_students = [
        s
        for c in classes
        for s in c["students"]
        if (lambda scores: sum(scores.values()) / 3 >= 90)(s["scores"])
    ]

    return {"averages": averages, "top_students": top_students}


# --------------------------

# 主程序交互

# --------------------------

if __name__ == "__main__":

    # 添加新学生

    new_student = {
        "id": 2002,
        "name": "墨大夫",
        "scores": {"炼丹术": 96, "御剑术": 85, "阵法": 90},
    }

    add_student(1, new_student)  # 添加到金丹二班

    # 查询学生信息

    target = find_student(1001)

    print(f"找到学生：{target['name']}，炼丹术成绩：{target['scores']['炼丹术']}")

    # 生成分析报告

    report = analyze_scores()

    print("\n=== 全年级成绩分析 ===")

    print(f"各科平均分：{report['averages']}")

    print(f"优秀学生名单：{[s['name'] for s in report['top_students']]}")
