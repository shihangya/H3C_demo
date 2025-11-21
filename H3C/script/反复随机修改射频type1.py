import pytest_atf
import random
pytest_atf.noatf_mode()
import os, re, string
from datetime import datetime
from AtfLibrary.topology import TopologyMap
from AtfLibrary.product import Terminal, CCmwDevice
import time
from function.miji import connect

AC = connect("AC")
AP = connect("AC")

#定义 radio 和 type

type_radios1 = ["dot11abe","dot11a","dot11abe","dot11ac","dot11abe","dot11an"]
type_radios2 = ["dot11b ", "dot11g", "dot11gax", "dot11gbe", "dot11gn"]


def AP_down():

    AP.send(f"""
                    Ctrl+z
                    reset wlan ap
                    """ )


i = 1
a = "g"
while True:
    for i in type_radios1:
        AC.send(f"""
                    wlan ap 7230
                    ra 1
                    type {i}
                    y
                    y
                    """ )
        time.sleep(1)
        AP_down()
        AC.send(f"""
                    probe
                    dis system internal wlan private-info ap 2 | in MLO
                    dis system internal wlan private-info ap 2 mlo
                    dis wlan bss ap 7230
                            """)

    for n in type_radios2:
        AC.send(f"""
                    wlan ap 7230
                    ra 2
                    type {n}
                    y
                    y

                    """)
        time.sleep(1)
        AP_down()
        AC.send(f"""
                    probe
                    dis system internal wlan private-info ap 2 | in MLO
                    dis system internal wlan private-info ap 2 mlo
                    dis wlan bss ap 7230
                            """)







