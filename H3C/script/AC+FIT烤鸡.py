import pytest_atf
import random

pytest_atf.noatf_mode()
import os, re, string
from datetime import datetime
from H3C.function.miji import connect
from AtfLibrary.topology import TopologyMap
from AtfLibrary.product import Terminal, CCmwDevice
import time

dut = connect("wx2520x-li-tM")

radios = ["radio 1", "radio 2"]
type_radios1 = ["dot11abe ", "dot11ac", "dot11an", "dot11ax"]
type_radios2 = ["dot11b ", "dot11g", "dot11gax", "dot11gbe", "dot11gn"]
flexible = ["mlo flexible-mode disable", "mlo flexible-mode enable"]
service_template = ("wpa3-h2e")

selected_radio = random.choice(radios)
selected_type = random.choice(type_radios1)
selected_type2 = random.choice(type_radios2)

while True:
    selected_flexible = random.choice(flexible)
    dut.send(f"""
                wlan ap ap7
                {selected_flexible}
                radio 1
                radio disable
                radio enable
                type {selected_type}
                Y
                Y
                radio 2
                radio disable
                radio enable
                type {selected_type2}
                Y
                Y
                radio 1
                service-template {service_template}
                radio 2
                service-template {service_template}
                radio 1
                undo service-template {service_template}
                radio 2
                undo service-template {service_template}
            """)

    time.sleep(2)




