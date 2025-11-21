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


def CheckApOnline(access_name,ip_address):
    # 使用connect函数获取设备实例
    dut = connect(access_name)
    Scmd = 'ping ' + ip_address
    # 执行命令检查AP是否在线，并判断结果
    result = dut.CheckCommand('AP是否在线',
                              cmd=Scmd,
                              expect=['5 packet(s) transmitted, 5 packet(s) received, 0.0% packet loss'],
                              expect_count=1,
                              stop_max_attempt=2,
                              relationship='and',
                              wait_fixed=2
                              )

    if result:
        print("AP在线")
        return True
    else:
        print("AP不在线")
        return False




def CheckAny(access_name,expect_str,cmd_txt,expect_list,expect_count):
    # 使用connect函数获取设备实例
    dut = connect(access_name)
    Scmd = cmd_txt
    # 执行命令检查AP是否在线，并判断结果
    result = dut.CheckCommand(expect_str,
                              cmd=Scmd,
                              expect=expect_list,
                              expect_count=expect_count,
                              stop_max_attempt=3,
                              relationship='and',
                              wait_fixed=3
                              )
    if result:
        print("检查通过")
        return 1
    else:
        print("检查不通过")
        return 2


def CheckAny_not(access_name,not_expect_str,cmd_txt,expect_list):
    # 使用connect函数获取设备实例
    dut = connect(access_name)
    Scmd = cmd_txt
    # 执行命令检查AP是否在线，并判断结果
    result = dut.CheckCommand(not_expect=not_expect_str,
                              cmd=Scmd,
                              expect=expect_list,
                              stop_max_attempt=2,
                              wait_fixed=2
                              )
    if result:
        print("检查通过")
        return 1
    else:
        print("检查不通过")
        return 2


def MackLog():
    import sys

    import os
    log_dir = r'D:\H3C_demo\H3C\log'
    os.makedirs(log_dir, exist_ok=True)

    # 创建带时间戳的日志文件
    now = datetime.now()
    log_file = open(f'{log_dir}\\execution_log_{now.strftime("%Y%m%d_%H%M%S")}.txt', 'w', encoding='utf-8')
    sys.stdout = log_file