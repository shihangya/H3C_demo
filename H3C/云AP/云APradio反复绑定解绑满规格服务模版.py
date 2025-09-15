import pytest_atf
import random

pytest_atf.noatf_mode()
import os, re, string
from datetime import datetime

from AtfLibrary.topology import TopologyMap
from AtfLibrary.product import Terminal, CCmwDevice
import time

finder = TopologyMap()

ternl = Terminal()
ternl.access_name = "7230"
ternl.open_window()
dut = CCmwDevice()
dut.add_terminal(ternl)
dut.topofinder = finder


import random
import time

from AtfLibrary.product import CCmwDevice
# 假设 dut、Terminal 等已定义并初始化

# 服务模板
service_template1 = ("g0", "g1", "g2", "g3", "g4", "g5", "g6", "g7", "g8", "g9", "g10", "g11", "g12", "g13", "g14", "g15")
service_template2 = ("g0", "g1", "g2", "g3", "g4", "g5", "g6", "g7", "g8", "g9", "g10", "g11", "g12", "g13", "g14", "g15")

mode = 0  # 控制先绑定还是先解绑：0=绑定，1=解绑


def get_shuffled_with_same_prefix(template1, template2):
    """
    返回两个打乱顺序的服务模板列表，前两个元素相同。
    """
    common_elements = list(set(template1) & set(template2))
    # print(common_elements)
    if len(common_elements) < 2:
        raise ValueError("两个服务模板中没有足够的共同元素来构成前两个相同的项")

    prefix = random.sample(common_elements, 2)

    rest1 = [x for x in template1 if x not in prefix]
    rest2 = [x for x in template2 if x not in prefix]

    random.shuffle(rest1)
    random.shuffle(rest2)

    return prefix + rest1,  rest2 + prefix


while True:
    if mode % 2 == 0:
        print("当前为绑定模式")
        shuffled_service1, shuffled_service2 = get_shuffled_with_same_prefix(service_template1, service_template2)
        print("radio1下的为：", shuffled_service1)
        print("radio2下的为：", shuffled_service2)

        for i in shuffled_service1:
            dut.send(f"""
                        interface WLAN-Radio 1/0/1
                        service-template {i}                                        
                                     """)
        for j in shuffled_service2:
            dut.send(f"""
                        interface WLAN-Radio 1/0/2
                        service-template {j}
                        interface WLAN-Radio 1/0/3
                        service-template {j}
                         """)
    else:
        print("当前为解绑模式")
        shuffled_service1, shuffled_service2 = get_shuffled_with_same_prefix(service_template1, service_template2)
        print("radio1下的为：", shuffled_service1)
        print("radio2下的为：", shuffled_service2)

        for i in shuffled_service1:
            dut.send(f"""
                        interface WLAN-Radio 1/0/1
                        undo service-template {i}                                        
                                     """)
        for j in shuffled_service2:
            dut.send(f"""
                        interface WLAN-Radio 1/0/2
                        undo service-template {j}
                        interface WLAN-Radio 1/0/3
                        undo service-template {j}
                         """)

        # for i in shuffled_service1:
        #     for j in shuffled_service2:
        #         dut.send(f"""
        #                     interface WLAN-Radio 1/0/1
        #                     undo service-template {i}
        #                     interface WLAN-Radio 1/0/2
        #                     undo service-template {j}
        #                     interface WLAN-Radio 1/0/3
        #                     undo service-template {j}
        #                  """)

    mode += 1
    time.sleep(4)








