import time
import random


def retry_operation(max_retries=3, delay=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"重试 {retries+1}/{max_retries}，原因：{e}")
                    retries += 1
                    time.sleep(delay)
            raise Exception("超过最大重试次数")

        return wrapper

    return decorator


@retry_operation(max_retries=5)
def connect_server():
    # 模拟不稳定的连接
    if random.random() < 0.7:
        raise ConnectionError("连接失败")
    return "连接成功"
