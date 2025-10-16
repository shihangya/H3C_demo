import datetime
import time

def calculate_work_time_and_earnings():
    """
    计算距离下班还有多久，并计算已到手的工资
    """
    # 设置工作时间参数
    work_start_time = datetime.time(9, 30)  # 上班时间：9:30
    work_end_time = datetime.time(18, 0)   # 下班时间：18:00
    hourly_wage = 47  # 每小时工资（元）

    # 获取当前时间
    now = datetime.datetime.now()
    current_time = now.time()

    # 计算剩余工作时间
    start_datetime = datetime.datetime.combine(now.date(), work_start_time)
    end_datetime = datetime.datetime.combine(now.date(), work_end_time)

    # 如果当前时间在上班时间内
    if work_start_time <= current_time <= work_end_time:
        remaining_time = end_datetime - now
        hours_worked = (now - start_datetime).total_seconds() / 3600

        # 计算已到手的工资
        earnings = hours_worked * hourly_wage

        print(f"⏰ 距离下班还有: {remaining_time}")
        print(f"💼 已工作: {hours_worked:.2f} 小时")
        print(f"💰 已到手工资: {earnings:.2f} 元")

    elif current_time < work_start_time:
        print("🕒 还未到上班时间")
    else:
        print("🎉 已经下班了！")

# 主循环，每秒更新一次
if __name__ == "__main__":
    while True:
        calculate_work_time_and_earnings()
        time.sleep(1)
