# -*- encoding=utf8 -*-
__author__ = "hys48682"

from airtest.core.api import *
from airtest.cli.parser import cli_setup

if not cli_setup():
    auto_setup(__file__, logdir=None, devices=["Android:///92232c6b",])


from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)


# script content
print("start...")


# generate html report
# from airtest.report.report import simple_report
# simple_report(__file__, logpath=None)
while True:
    poco(text="00*hnp-wa7638cloud*").click()
    poco(text="00*h2e-wa7638cloud*").click()



