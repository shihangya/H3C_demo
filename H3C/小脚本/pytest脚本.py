# *-* encoding: utf-8 *-*
# 如下库必须导入，可根据需要导入其它库
import sys
import os
import re
import time
import pytest_atf

pytest_atf.noatf_mode()
from datetime import datetime
from AtfLibrary.topology import TopologyMap
from AtfLibrary.product import Terminal, CCmwDevice

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resource'))
print(sys.path)
from VarsAndFuncs import VarsAndFuncs as VF
from read_excel import read_xlsx
import random

# 创建cmw设备的Terminal
term1 = Terminal()
term1.access_name = "ac2_tel"  # 设备控制台窗口的名字（需要根据实际情况修改）
term1.open_window()
# 创建cmw设备对象
AC = CCmwDevice()
AC.add_terminal(term1)
finder = TopologyMap()
AC.topofinder = finder
# 创建cmw设备的Terminal
# term2 = Terminal()
# term2.access_name = 'TEL-WA7539'           #设备控制台窗口的名字（需要根据实际情况修改）
# term2.open_window()
# # 创建cmw设备对象
# AP = CCmwDevice()
# AP.add_terminal(term2)
# finder = TopologyMap()
# AP.topofinder = finder

# 脚本对应用例的信息，case_no 必须与用例编号对应
module = '服务模板'
case_no = 'T24_P6106'


class TestClass:
    '''
    测试目的：拷机
    '''

    @classmethod
    def setup_class(cls):
        '''
        脚本初始配置
        '''
        cmd = f"""{VF.user_view}
        screen-length disable
        u t d
        u t m
        system-view
        undo info-center enable
        """
        AC.send(cmd)
        ###配置服务模板
        for i in range(3,513):
            cmd = f"""{VF.system_view}
            wlan service-template st{i}
            ssid 16136_mlo_{i}
            {VF.wpa3_psk_h2e}
            service-template enable
            quit
            """
            AC.send(cmd)
        for i in range(1,3):
            cmd = f"""{VF.system_view}
            wlan service-template st{i}
            ssid 16136_mlo_{i}
            {VF.wpa3_psk_h2e}
            mlo enable
            service-template enable
            quit
            """
            AC.send(cmd)

    @classmethod
    def teardown_class(cls):
        '''

        '''
        ##AC开启ap控制台
        pass

    def test_step_1(self):
        '''

        '''
        for i in range(1, 513):
            AC.send(f"""wlan ap 0011-2{hex(i - 1)[2:].zfill(3)}-0000""")
            all_templates = list(range(3, 513))
            # random.shuffle(all_templates) #打乱顺序
            rd_template = random.sample(all_templates, 4)
            rd_template.extend([1, 2])
            random.shuffle(rd_template)
            for i in rd_template:
                AC.send(f"""
                        radio 1
                        service-template st{i}
                        """)
            rd_template1 = random.sample(all_templates, 4)
            rd_template1.extend([1, 2])
            random.shuffle(rd_template1)
            for i in rd_template1:
                AC.send(f"""
                        radio 2
                        service-template st{i}
                        """)
            # random.shuffle(all_templates) #打乱顺序
            rd_template2 = random.sample(all_templates, 4)
            rd_template2.extend([1, 2])
            random.shuffle(rd_template2)
            for i in rd_template2:
                AC.send(f"""
                        radio 3
                        service-template st{i}
                        """)
            AC.send("quit")
            # AC.send("dis wlan bss all")
        time.sleep(50)
    # def test_step_2(self):
    #     '''

    #     '''
    #     for i in range(1,513):
    #         AC.send(f"""wlan ap 0011-2{hex(i-1)[2:].zfill(3)}-0000""")
    #         all_templates = list(range(1, 17))
    #         a = random.choice(all_templates)
    #         AC.send(f"""
    #                 radio 2
    #                 undo service-template stp{a}
    #                 """)

    #         b = random.choice(all_templates)
    #         AC.send(f"""
    #                 radio 3
    #                 undo service-template stp{b}
    #                 """)
    #         AC.send("quit")
    #         AC.send("dis wlan bss all")
    #     time.sleep(50)
    #     for i in range(1,2):
    #         AC.send(f"""wlan ap 0011-2{hex(i-1)[2:].zfill(3)}-0000""")
    #         AC.send(f"""
    #                 radio 2
    #                 service-template stp{a}
    #                 """)

    #         AC.send(f"""
    #                 radio 3
    #                 service-template stp{b}
    #                 """)
    #         AC.send("quit")
    #         AC.send("dis wlan bss all")


if __name__ == "__main__":
    test = TestClass()
    test.setup_class()
    test.test_step_1()
    # for i in range(1,1000):
    #     test.test_step_2()
