import pyautogui
import time

def anti_sleep_mouse():
    """防止电脑进入休眠状态的小幅度鼠标移动"""
    # 获取当前鼠标位置
    current_x, current_y = pyautogui.position()

    move_distance = 2  # 移动距离

    try:
        while True:
            # 小幅度移动鼠标
            pyautogui.moveRel(move_distance, 0, duration=0.1)
            time.sleep(60)
            pyautogui.moveRel(-move_distance, 0, duration=0.1)
            time.sleep(60)  # 每分钟移动一次

    except KeyboardInterrupt:
        print("防休眠脚本已停止")

if __name__ == "__main__":
    print("防休眠鼠标移动启动，按 Ctrl+C 停止")
    anti_sleep_mouse()
