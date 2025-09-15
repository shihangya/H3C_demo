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
ternl.access_name = "7220-hi1"
ternl.open_window()
dut = CCmwDevice()
dut.add_terminal(ternl)
dut.topofinder = finder

radios = ["interface WLAN-Radio 1/0/1", "interface WLAN-Radio 1/0/2"]
type_radios1 = ["dot11a","dot11abe ","dot11abe ","dot11abe ", "dot11ac", "dot11an", "dot11ax","dot11be","dot11be","dot11be","dot11eax"]
type_radios2 = ["dot11gax", "dot11gn", "dot11gbe", "dot11gbe", "dot11gbe"]
channal_band_list1 = ["20","40"]
channal_band_list2 = ["20","40"]

selected_radio = random.choice(radios)
selected_type = random.choice(type_radios1)
selected_channal_band1 = random.choice(channal_band_list1)
selected_channal_band2 = random.choice(channal_band_list1)

for i in range(50000):
    selected_radio = random.choice(radios)


    # 根据 radio 选择对应的 type
    if selected_radio == "interface WLAN-Radio 1/0/1":
        selected_type = random.choice(type_radios1)
        selected_channals_band = random.choice(channal_band_list1)
    elif selected_radio == "interface WLAN-Radio 1/0/2":
        selected_type = random.choice(type_radios2)
        selected_channals_band = random.choice(channal_band_list2)

    # dut.send(f"""
    #             {selected_radio}
    #             shutdown
    #             undo shutdown
    #
    #         """)
    # time.sleep(17)
    # 创建服务模版
    dut.send(f"""
                {selected_radio}
                shutdown
                undo shutdown
                type {selected_type}
                Y
                Y
                channel band-width {selected_channals_band}
                Y
                Y
            """)
    time.sleep(17)




