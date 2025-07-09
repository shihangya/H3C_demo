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


radios = ["radio 1", "radio 2"]
type_radios1 = ["dot11abe ", "dot11ac", "dot11an", "dot11ax"]
type_radios2 = ["dot11b ", "dot11g", "dot11gax", "dot11gbe", "dot11gn"]
flexible = ["wlan mlo flexible-mode disable", "wlan mlo flexible-mode enable"]
service_template = ("wpa3-h2e")

selected_radio = random.choice(radios)
selected_type = random.choice(type_radios1)
selected_type2 = random.choice(type_radios2)

while True:
    selected_flexible = random.choice(flexible)
    dut.send(f""" 
                {selected_flexible}
                interface WLAN-Radio 1/0/1
                shutdown
                undo shutdown
                type {selected_type}
                Y
                Y
                interface WLAN-Radio 1/0/2
                shutdown
                undo shutdown
                type {selected_type2}
                Y
                Y
                interface WLAN-Radio 1/0/1
                service-template {service_template}
                interface WLAN-Radio 1/0/2
                service-template {service_template}
                interface WLAN-Radio 1/0/1
                undo service-template {service_template}
                interface WLAN-Radio 1/0/2
                undo service-template {service_template}
                quit
            """)

    time.sleep(2)




