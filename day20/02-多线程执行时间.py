import threading
import time


def task(name):
    print(f"{name} 开始工作")
    time.sleep(2)
    print(f"{name} 工作完成")

start = time.time()
threads = []
for i in range(1, 4):
    t = threading.Thread(target=task, args=(f"工人{i}",))
    threads.append(t)
    t.start()
for t in threads:
    t.join()  # 等待所有线程完成

end = time.time()
print(f"总耗时{end - start}秒")
