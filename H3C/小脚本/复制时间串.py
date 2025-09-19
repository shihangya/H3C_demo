import datetime
import pyperclip

# 获取当前时间
current_time = datetime.datetime.now()

print(current_time)
# 格式化时间为 202509251025 格式
formatted_time = current_time.strftime("%Y%m%d%H%M")

# 复制到剪切板
pyperclip.copy(formatted_time)

print(f"当前时间已复制到剪切板: {formatted_time}")


