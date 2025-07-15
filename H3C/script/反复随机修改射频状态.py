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
ternl.access_name = "wx2520x-li-tM"
ternl.open_window()
dut = CCmwDevice()
dut.add_terminal(ternl)
dut.topofinder = finder


radios = ["radio 1", "radio 2"]
type_radios1 = ["dot11abe ", "dot11ac", "dot11an", "dot11ax"]
type_radios2 = ["dot11b ", "dot11g", "dot11gax", "dot11gbe", "dot11gn"]


selected_radio = random.choice(radios)
selected_type = random.choice(type_radios1)


a = "g"
for i in range(20):
    b = a + str(i)
    selected_radio = random.choice(radios)

    # 根据 radio 选择对应的 type
    if selected_radio == "radio 1":
        selected_type = random.choice(type_radios1)
    elif selected_radio == "radio 2":
        selected_type = random.choice(type_radios2)
    else:
        selected_type = ""  # 可选默认处理
    # 创建服务模版
    dut.send(f"""
                wlan ap ap7
                {selected_radio}
                radio disable
                radio enable
            """)
    time.sleep(2)




