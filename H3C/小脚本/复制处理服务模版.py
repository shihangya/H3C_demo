import pyperclip
import re

def convert_to_undo_commands():
    # 从剪贴板读取内容
    clipboard_content = pyperclip.paste()

    # 分割成行
    lines = clipboard_content.strip().split('\n')

    # 存储转换后的命令
    undo_commands = []

    # 匹配 service-template 命令并转换为 undo 命令
    for line in lines:
        line = line.strip()
        # 匹配 "service-template <template_name>" 模式
        match = re.match(r'^\s*service-template\s+(\S+)', line)
        if match:
            template_name = match.group(1)
            undo_command = f"undo service-template {template_name}"
            undo_commands.append(undo_command)

    # 将转换后的命令写回剪贴板
    result = '\n'.join(undo_commands)
    pyperclip.copy(result)

    print("转换完成！结果已复制到剪贴板：")
    print(result)

if __name__ == "__main__":
    convert_to_undo_commands()
