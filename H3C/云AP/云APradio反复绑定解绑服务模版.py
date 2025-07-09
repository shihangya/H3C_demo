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




service_template = ("wpa3-h2e")

while True:
    dut.send(f"""
                interface WLAN-Radio 1/0/1
                service-template {service_template}
                interface WLAN-Radio 1/0/2
                service-template {service_template}
                interface WLAN-Radio 1/0/1
                undo service-template {service_template}
                interface WLAN-Radio 1/0/2
                undo service-template {service_template}
            """)





