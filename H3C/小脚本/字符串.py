import secrets
import string

# 定义字符集（大小写字母+数字）
characters = string.ascii_letters + string.digits

# 生成250位随机字符串
random_string = ''.join(secrets.choice(characters) for _ in range(250))

print(random_string)