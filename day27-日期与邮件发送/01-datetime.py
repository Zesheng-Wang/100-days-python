from datetime import datetime, timedelta

import pytz  # 需安装pytz

# 创建特定时区时间

tz_shanghai = pytz.timezone("Asia/Shanghai")
now = datetime.now(tz_shanghai)
print(f"上海时间: {now.strftime('%Y-%m-%d %H:%M:%S %Z')}")

# 时间间隔计算
new_year = datetime(2026, 1, 1, tzinfo=tz_shanghai)
countdown = new_year - now
print(f"距离2026新年还有: {countdown.days}天 {countdown.seconds//3600}小时")


# 周期性任务判断
def is_weekday(date):
    return 0 <= date.weekday() < 5


print(f"今天是否工作日: {is_weekday(now)}")
