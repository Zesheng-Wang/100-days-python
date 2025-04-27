import requests


# 示例：调用天气API
def get_weather(city):
    # 通过API端点获取数据
    response = requests.get(f"<https://api.weather.com/{city}>")
    # 解析返回的JSON格式数据
    return response.json()["temperature"]


print(get_weather("shanghai"))
