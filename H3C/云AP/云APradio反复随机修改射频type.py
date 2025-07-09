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
ternl.access_name = "WA7220H"
ternl.open_window()
dut = CCmwDevice()
dut.add_terminal(ternl)
dut.topofinder = finder

radios = ["interface WLAN-Radio 1/0/1", "interface WLAN-Radio 1/0/2"]
type_radios1 = ["dot11a","dot11abe ", "dot11ac", "dot11an", "dot11ax"]
type_radios2 = ["dot11b ", "dot11g", "dot11gax", "dot11gbe", "dot11gn"]


selected_radio = random.choice(radios)
selected_type = random.choice(type_radios1)

i = 1
a = "g"
for i in range(50000):
    b = a + str(i)
    selected_radio = random.choice(radios)

    # 根据 radio 选择对应的 type
    if selected_radio == "interface WLAN-Radio 1/0/1":
        selected_type = random.choice(type_radios1)
    elif selected_radio == "interface WLAN-Radio 1/0/2":
        selected_type = random.choice(type_radios2)
    else:
        selected_type = ""  # 可选默认处理
    # 创建服务模版
    dut.send(f"""
                {selected_radio}
                shutdown
                undo shutdown
                type {selected_type}
                Y
                Y
            """)
    i = i + 1
    time.sleep(2)




