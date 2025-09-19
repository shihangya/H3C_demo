import locale
import subprocess

# 创建一个子进程，但不等待它完成
process = subprocess.Popen(['ping', '77.88.0.66'], stdout=subprocess.PIPE)

# 读取子进程的输出
output, _ = process.communicate()

# 打印输出
system_encoding = locale.getpreferredencoding()
print(output.decode(system_encoding))

# 检查返回值
if process.returncode == 0:
    print("Ping 成功")
else:
    print("Ping 失败")
