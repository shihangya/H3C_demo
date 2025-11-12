# -*- encoding=utf8 -*-
__author__ = "hys48682"

import time

from airtest.core.api import *
from airtest.cli.parser import cli_setup
from function.miji import *
from function.service import *

MackLog()

if not cli_setup():
    auto_setup(__file__, logdir=None, devices=["Android:///ZY22GCD32Q", ])

from poco.drivers.android.uiautomation import AndroidUiautomationPoco

poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

# script content
print("start...")

AC = connect("2520x1")
# generate html report
# from airtest.report.report import simple_report
# simple_report(__file__, logpath=None)
while True:
    try:
        # 连接WiFi
        connect_result = connect_to_wifi("ZY22GCD32Q", "0202035888", "123123123")
        print(f"WiFi连接结果: {connect_result}")
    except Exception as e:
        print(f"WiFi连接异常: {e}")

    try:

        # 发送命令
        AC.send(f'''
                        dis wlan client
                        dis wlan client v | in MLO

                      '''
                )
    except Exception as e:
        print(f"发送命令异常: {e}")

    try:
        keyevent("HOME")
        time.sleep(1)
        poco("设置").click()

        time.sleep(1)
        touch(Template(r"tpl1761704087715.png", record_pos=(0.365, -0.091), resolution=(1080, 2400)))
        time.sleep(1)
        touch(Template(r"tpl1761704101396.png", record_pos=(-0.306, -0.042), resolution=(1080, 2400)))
        time.sleep(1)




    except Exception as e:
        print(f"UI操作异常: {e}")






















