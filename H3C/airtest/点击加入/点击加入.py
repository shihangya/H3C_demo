# -*- encoding=utf8 -*-
__author__ = "hys48682"

import time

from airtest.core.api import *
from airtest.cli.parser import cli_setup
from function.miji import *
from function.service import *

MackLog()

if not cli_setup():
    auto_setup(__file__, logdir=None, devices=["Android:///Z5Y5KZY9LZRS69JF",])


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
        connect_result = connect_to_wifi("Z5Y5KZY9LZRS69JF", "0202035888", "123123123")
        print(f"WiFi连接结果: {connect_result}")
    except Exception as e:
        print(f"WiFi连接异常: {e}")
    #
    # try:
    #
    #     # 发送命令
    #     AC.send(f'''
    #                     dis wlan client
    #                     dis wlan client v | in MLO
    #
    #                   '''
    #             )
    # except Exception as e:
    #     print(f"发送命令异常: {e}")

    try:
        
        keyevent("HOME")
        touch(Template(r"tpl1763013041091.png", record_pos=(0.188, 0.923), resolution=(1240, 2772)))
        touch(Template(r"tpl1763012886891.png", record_pos=(-0.198, -0.347), resolution=(1240, 2772)))
        touch(Template(r"tpl1763012897511.png", record_pos=(-0.004, -0.305), resolution=(1240, 2772)))
        touch(Template(r"tpl1763012908444.png", record_pos=(0.232, 0.952), resolution=(1240, 2772)))


    except Exception as e:
        print(f"UI操作异常: {e}")



















