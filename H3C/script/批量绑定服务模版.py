from function import *
import time
import re

# 连接到 AC 控制器
AC = connect("wx5560X")

def refresh_ap_radio_config():
    # 第一步：显示所有 AP 的信息
    output = AC.send("display wlan ap all")
    time.sleep(2)  # 等待输出返回完整

    # 第二步：正则匹配出 WA7538 型号的 AP 名称
    ap_lines = re.findall(r'\s+(\S+)\s+\d+\s+\S+\s+WA7638\s+', output)
    print("找到的 WA7638 AP 列表:", ap_lines)

    # 第三步：对每个 AP 执行配置刷新
    for ap_name in ap_lines:
        print(f"正在处理 AP: {ap_name}")
        AC.send( f'''
                    wlan ap {ap_name}
                    radio 1
                    radio enable
                    undo service-template duoap
                    undo service-template g1
                    service-template g1
                    service-template duoap
                    exit
                    radio 2
                    radio enable
                    undo service-template duoap
                    undo service-template g1
                    service-template g1
                    service-template duoap
                    exit
                    radio 3
                    radio enable
                    undo service-template duoap
                    undo service-template g1
                    service-template g1
                    service-template duoap
        '''
        )
        
        time.sleep(3)  # 每个 AP 配置后等待一下

# 主循环：每隔 5 分钟执行一次
try:
    while True:
        refresh_ap_radio_config()
        print("等待下一次执行...")
        time.sleep(300)  # 等待 5 分钟
except KeyboardInterrupt:
    print("脚本已手动终止。")