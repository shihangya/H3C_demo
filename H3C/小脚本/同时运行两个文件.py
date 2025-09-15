import subprocess
import sys

# 定义要运行的两个 Python 文件
script1 = 'a.py'  # 替换为你的第一个脚本名
script2 = 'b.py'  # 替换为你的第二个脚本名

def run_script(script_name):
    """运行指定的 Python 脚本"""
    try:
        process = subprocess.Popen([sys.executable, script_name])
        return process
    except Exception as e:
        print(f"无法运行 {script_name}: {e}")
        return None

if __name__ == "__main__":
    print("正在启动两个脚本...")

    # 并行启动两个脚本
    proc1 = run_script(script1)
    proc2 = run_script(script2)

    # 等待两个脚本执行完成（可选）
    if proc1:
        proc1.wait()
    if proc2:
        proc2.wait()

    print("两个脚本均已结束。")