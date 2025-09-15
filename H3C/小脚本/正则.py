import re

text = "abcd efg d kl afd af af asfa adf aHello123_fa 123Hell_owo Hello123$%^ afbcdafjk zvk;ajkfa He12lo_a ABc1_234"

pattern = r'(?=^.{8,15}$)(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*_)[A-Za-z0-9_]+'

# 分割文本为单词后逐个匹配
words = text.split()
matches = []
for word in words:
    if re.fullmatch(pattern, word):
        matches.append(word)

print("匹配结果：", matches)
# 输出示例：['He12lo_a', 'ABc1_234']

#
# import random
# import string
#
# def generate_password():
#     # 定义字符集
#     lower = string.ascii_lowercase      # a-z
#     upper = string.ascii_uppercase      # A-Z
#     digits = string.digits              # 0-9
#     special = '_'                       # 下划线
#     all_chars = lower + upper + digits + special
#
#     # 随机选择密码长度（8 到 10）
#     length = random.randint(8, 10)
#
#     # 确保每类字符至少出现一次
#     password = [
#         random.choice(lower),
#         random.choice(upper),
#         random.choice(digits),
#         random.choice(special)
#     ]
#
#     # 填充剩余长度
#     for _ in range(length - 4):
#         password.append(random.choice(all_chars))
#
#     # 打乱顺序，避免固定模式
#     random.shuffle(password)
#
#     # 转为字符串
#     return ''.join(password)
#
# # === 示例使用 ===
# if __name__ == "__main__":
#     print("生成的密码：")
#     for _ in range(5):  # 生成 5 个示例密码
#         print(generate_password())