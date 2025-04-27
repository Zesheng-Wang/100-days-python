import requests


def get_question():
    """获取天机题库问题"""
    params = {
        "amount": 1,
        "type": "multiple",  # 多选题
        "category": 18,  # 计算机类
        "encode": "url3986",  # 编码格式
    }

    try:
        response = requests.get("https://opentdb.com/api.php", params=params, timeout=5)
        data = response.json()
        return data["results"][0]
    except Exception as e:
        print(f"天机获取失败: {str(e)}")
        return None


result = get_question()
print(result)
# 示例数据结构
"""
{
    'category': 'Science: Computers',
    'type': 'multiple',
    'difficulty': 'easy',
    'question': 'HTML是什么的缩写？',
    'correct_answer': 'Hyper Text Markup Language',
    'incorrect_answers': ['..."]
}
"""
{
    "type": "multiple",
    "difficulty": "easy",
    "category": "Science%3A%20Computers",
    "question": "What%20programming%20language%20was%20GitHub%20written%20in%3F",
    "correct_answer": "Ruby",
    "incorrect_answers": ["JavaScript", "Python", "Lua"],
}
