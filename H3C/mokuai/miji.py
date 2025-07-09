import pytest_atf
import random

pytest_atf.noatf_mode()
import os, re, string
from datetime import datetime

from AtfLibrary.topology import TopologyMap
from AtfLibrary.product import Terminal, CCmwDevice
import time

def connect(access_name):

    finder = TopologyMap()
    ternl = Terminal()
    ternl.access_name = access_name
    ternl.open_window()
    dut = CCmwDevice()
    dut.add_terminal(ternl)
    dut.topofinder = finder
    
    return dut

