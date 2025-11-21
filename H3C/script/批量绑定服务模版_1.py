from function import *
import time
import re

# 连接到 AC
AC = connect("2580_2")

def band_ap_radio_config():
    # 第一步：显示所有 AP 的信息
    output = AC.send("display wlan ap all")
    time.sleep(2)  # 等待输出返回完整

    # 第二步：正则匹配出 WA7538 型号的 AP 名称
    ap_lines = re.findall(r'\s+(\S+)\s+\d+\s+\S+\s+WA7538\s+', output)
    print("找到的 WA7539 AP 列表:", ap_lines)

    # 第三步：对每个 AP 绑定服务模版
    for ap_name in reversed(ap_lines):
        print(f"正在处理 AP: {ap_name}")

        AC.send( f'''
                    wlan ap {ap_name}
                    radio 1
                    radio enable
                    service-template m1
                    service-template m2
                    service-template m3
                    service-template m4
                    service-template m5
                    service-template m6
                    service-template m7
                    service-template m8
                    service-template m9
                    service-template m10
                    service-template m11
                    service-template m12
                    service-template m13
                    service-template m14
                    service-template m15
                    service-template m16
                    service-template m17
                    service-template m18
                    service-template m19
                    radio 2
                    radio enable
                    service-template m1
                    service-template m2
                    service-template m3
                    service-template m4
                    service-template m5
                    service-template m6
                    service-template m7
                    service-template m8
                    service-template m9
                    service-template m10
                    service-template m11
                    service-template m12
                    service-template m13
                    service-template m14
                    service-template m15
                    service-template m16
                    service-template m17
                    service-template m18
                    service-template m19
                    radio 3
                    radio enable
                    service-template m1
                    service-template m2
                    service-template m3
                    service-template m4
                    service-template m5
                    service-template m6
                    service-template m7
                    service-template m8
                    service-template m9
                    service-template m10
                    service-template m11
                    service-template m12
                    service-template m13
                    service-template m14
                    service-template m15                    
                    service-template m16
                    service-template m17
                    service-template m18
                    service-template m19

        '''
        )
        
        # time.sleep(3)  # 每个 AP 配置后等待一下


def unband_ap_radio_config():
    # 第一步：显示所有 AP 的信息
    output = AC.send("display wlan ap all")
    time.sleep(2)  # 等待输出返回完整

    # 第二步：正则匹配出 WA7538 型号的 AP 名称
    ap_lines = re.findall(r'\s+(\S+)\s+\d+\s+\S+\s+WA7538\s+', output)
    print("找到的 WA7539 AP 列表:", ap_lines)

    # 第三步：对每个 AP 绑定服务模版
    for ap_name in ap_lines:
        print(f"正在处理 AP: {ap_name}")

        AC.send(f'''
                    wlan ap {ap_name}
                    radio 1
                    radio enable
                    undo service-template wpa3-h2e
                    undo service-template wpa3-both
                    radio 2
                    radio enable
                    undo service-template wpa3-h2e
                    undo service-template wpa3-both
                    radio 3
                    radio enable
                    undo service-template wpa3-h2e
                    undo service-template wpa3-both

        '''
                )

def delete_all_ap():
    # 第一步：显示所有 AP 的信息
    output = AC.send("display wlan ap all")
    time.sleep(2)  # 等待输出返回完整

    # 第二步：正则匹配出 WA7538 型号的 AP 名称
    ap_lines = re.findall(r'\s+(\S+)\s+\d+\s+\S+\s+WA7538\s+', output)
    print("找到的 WA7539 AP 列表:", ap_lines)

    # 第三步：对每个 AP 执行配置刷新
    for ap_name in ap_lines:
        print(f"正在处理 AP: {ap_name}")
        AC.send(f'''
        undo wlan ap {ap_name}
        Y
        ''')


# 主循环：每隔 5 分钟执行一次
try:
    while True:
        band_ap_radio_config()
        print("等待下一次执行...")
        time.sleep(10)  # 等待 10 秒
except KeyboardInterrupt:
    print("脚本已手动终止。")