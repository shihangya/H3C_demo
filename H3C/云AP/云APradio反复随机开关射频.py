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
ternl.access_name = "wa7638"
ternl.open_window()
dut = CCmwDevice()
dut.add_terminal(ternl)
dut.topofinder = finder

radios = ["interface WLAN-Radio 1/0/1", "interface WLAN-Radio 1/0/2", "interface WLAN-Radio 1/0/3"]



selected_radio = random.choice(radios)



for i in range(50000):
    selected_radio = random.choice(radios)


    dut.send(f"""
                {selected_radio}
                shutdown
                undo shutdown
                type {selected_type}
                Y
                Y
            """)
    time.sleep(2)




