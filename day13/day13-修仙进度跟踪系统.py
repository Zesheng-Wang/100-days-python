import json
from functools import reduce
from datetime import datetime


def log_activity(action):
    """修炼日志装饰器"""

    def decorator(func):
        def wrapper(self, *args):
            print(f"{self.name}开始{action}...")
            result = func(self, *args)
            print(f"{action}完成！当前境界：{self.current_stage}")
            return result

        return wrapper

    return decorator


class CultivationTracker:
    def __init__(self):
        self.disciples = {}
        self._load_data()

    def _load_data(self):
        try:
            with open("cultivation.json", encoding='utf-8') as f:
                data = json.load(f)
                self.disciples = {
                    name: Cultivator(name, **stats) for name, stats in data.items()
                }
        except FileNotFoundError:
            pass

    def save_data(self):
        data = {
            name: {"stage": cult._stage, "last_breakthrough": cult.last_breakthrough}
            for name, cult in self.disciples.items()
        }
        with open("cultivation.json", "w") as f:
            json.dump(data, f)

    def add_disciple(self, name):
        if name not in self.disciples:
            self.disciples[name] = Cultivator(name)

    @log_activity("批量突破检测")
    def check_breakthroughs(self):
        return list(
            filter(lambda cult: cult.check_breakthrough(), self.disciples.values())
        )

    def power_ranking(self):
        return sorted(self.disciples.values(), key=lambda x: x.power, reverse=True)


class Cultivator:
    def __init__(self, name, stage=0, last_breakthrough=None):
        self.name = name
        self._stage = stage
        self.power = 1000 * (2**stage)
        self.last_breakthrough = last_breakthrough or datetime.now().isoformat()

    def check_breakthrough(self):
        if self.power >= 2000 * (2**self._stage):
            self._stage += 1
            self.last_breakthrough = datetime.now().isoformat()
            return True
        return False

    @log_activity("运转周天")
    def meditate(self, hours):
        self.power += hours * 10


# 使用示例
tracker = CultivationTracker()
tracker.add_disciple("韩立")
tracker.disciples["韩立"].power = 9800

print("=== 战力排行榜 ===")
for i, cult in enumerate(tracker.power_ranking(), 1):
    print(f"{i}. {cult.name}: {cult.power}")

tracker.save_data()
