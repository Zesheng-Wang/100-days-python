import random


# --------------------------
# 基础类定义
# --------------------------
class SpiritBeast:
    ELEMENTS = {
        "火": {"克": "金", "被克": "水"},
        "水": {"克": "火", "被克": "土"},
        "土": {"克": "水", "被克": "木"},
        "木": {"克": "土", "被克": "金"},
        "金": {"克": "木", "被克": "火"},
    }

    def __init__(self, name, element, power=100):
        self.name = name
        self.element = element
        self.power = power

    def check_element(self, target):
        """五行相克判定"""
        if self.element == self.ELEMENTS[target.element]["克"]:
            return 1.5  # 克制伤害加成
        elif self.element == self.ELEMENTS[target.element]["被克"]:
            return 0.5  # 被克伤害减免
        return 1.0

    def attack(self, target):
        damage = random.randint(10, 20) * self.check_element(target)
        target.power -= int(damage)
        print(f"{self.name}对{target.name}造成{int(damage)}点伤害！")

    def is_alive(self):
        return self.power > 0


# --------------------------
# 派生类定义
# --------------------------
class FirePhoenix(SpiritBeast):
    def __init__(self):
        super().__init__("朱雀", "火", 200)

    def special_skill(self):
        print("朱雀涅槃重生，恢复全部灵力！")
        self.power = 200


class WaterDragon(SpiritBeast):
    def __init__(self):
        super().__init__("玄武", "水", 180)

    def heal(self):
        recover = random.randint(20, 30)
        self.power += recover
        print(f"玄武引动水灵，恢复{recover}点灵力！")


# --------------------------
# 对战系统
# --------------------------
class BattleSystem:
    def __init__(self, beast1, beast2):
        self.beasts = [beast1, beast2]

    def start_battle(self):
        round = 1
        while all(b.is_alive() for b in self.beasts):
            print(f"\n=== 第{round}回合 ===")
            attacker, defender = random.sample(self.beasts, 2)

            # 特殊技能触发
            if isinstance(attacker, FirePhoenix) and random.random() < 0.3:
                attacker.special_skill()
            elif isinstance(attacker, WaterDragon) and random.random() < 0.3:
                attacker.heal()
            else:
                attacker.attack(defender)

            # 显示状态
            for b in self.beasts:
                print(f"{b.name} 剩余灵力：{b.power}")

            round += 1

        winner = next(b for b in self.beasts if b.is_alive())
        print(f"\n战斗结束！胜者：{winner.name}")


# --------------------------
# 启动对战
# --------------------------
if __name__ == "__main__":
    zhuque = FirePhoenix()
    xuanwu = WaterDragon()

    arena = BattleSystem(zhuque, xuanwu)
    arena.start_battle()