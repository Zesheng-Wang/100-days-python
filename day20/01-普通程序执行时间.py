import threading
import time
# 单线程示例
def task(name):
    print(f"{name} 开始工作")
    time.sleep(2)
    print(f"{name} 工作完成")
# 顺序执行（耗时约6秒）

start = time.time()

task("工人1")
task("工人2")
task("工人3")

end = time.time()
print(f"总耗时{end - start}秒")