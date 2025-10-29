import pytest_atf
pytest_atf.noatf_mode()
import os, re, string
from datetime import datetime
from .miji import connect  # ✅ 修改为相对导入
from AtfLibrary.topology import TopologyMap
from AtfLibrary.product import Terminal, CCmwDevice
import time
from .android import *


# dut = connect("qx-1240")



# def test(device_name,num):
#     """
#     创建服务模版
#     """
#     dut = connect(device_name)
#     a = "g"
#     for i in range(num):
#         b = a + str(i)
#         # 创建服务模版
#         dut.send(f"""
                    
#                     {device_name}
#                 """)
#         i = i + 1
    
# 服务模板
def set_service_template(device_name,num):
    """
    创建服务模版
    """
    dut = connect(device_name)
    a = "m"
    for i in range(num):
        b = a + str(i)
        # 创建服务模版
        dut.send(f"""
                    wlan service-template {b}
                    ssid {b}
                    
                    mlo enable
                    akm mode psk
                    preshared-key pass-phrase simple 123123123
                    cipher-suite ccmp
                    security-ie rsn
                    wpa3 personal mandatory
                    akm sae pwe h2e
                    pmf mandatory
                    service-template enable
                """)
        i = i + 1


def set_service_clear_template(device_name, num):
    """
    创建服务模版
    """
    dut = connect(device_name)
    a = "e"
    for i in range(num):
        b = a + str(i)
        # 创建服务模版
        dut.send(f"""
                    wlan service-template {b}
                    ssid {b}
                     enhanced-open enable
                    service-template enable
                """)
        i = i + 1


def set_radio_service_template(device_name,num):
    """
    radio 下绑定服务模版
    """
    dut = connect(device_name)
    a = "g"
    for i in range(num):
        b = a + str(i)
        # radio 下绑定
        dut.send(f"""
                radio 1
                service-template {b}
                radio 2
                service-template {b}
                radio 3
                service-template {b}

            """)
    i = i+1
    

    
def cloud_ap_radio_service_template(device_name,num):
    """
    cloud AP radio 下绑定服务模版
    """
    dut = connect(device_name)
    a = "g"
    for i in range(num):
        b = a + str(i)
        # cloud AP radio 下绑定
        dut.send(f"""
                interface WLAN-Radio 1/0/1
                service-template {b}
                interface WLAN-Radio 1/0/2
                service-template {b}
                interface WLAN-Radio 1/0/3
                service-template {b}
                """
        )
        i = i + 1
        
def cloud_ap_radio_service_template_undo(device_name,num):
    """
    cloud AP radio 下解绑定服务模版
    """
    dut = connect(device_name)
    a = "g"
    for i in range(num):
        b = "wpa3-h2e"
        # cloud AP radio 下解绑定
        dut.send(f"""
                interface WLAN-Radio 1/0/1
                undo service-template {b}
                interface WLAN-Radio 1/0/2
                undo service-template {b}
                interface WLAN-Radio 1/0/3
                undo service-template {b}
                """)
        i = i + 1

def ap_radio_service_template_undo(device_name,num):
    """
    radio 下解绑定服务模版
    """
    dut = connect(device_name)
    a = "g"
    for i in range(num):
        b = a + str(i)
        # radio 下解绑定
        dut.send(f"""
                    radio 1
                    undo service-template {b}
                    Y
                    radio 2
                    undo service-template {b}
                    Y
                    radio 3
                    undo service-template {b}
                    Y
                """)
        i = i+1

def delete_service_template(device_name,num):
    """
    删除服务模版
    """
    dut = connect(device_name)
    a = "g"
    for i in range(num):
        b = a + str(i)
        # 删除服务模版
        dut.send(f"""
                    undo wlan service-template {b}
                """)
        i = i+1

def delete_service_template_name(device_name,apname,ser_name):
    """
    按名字删除服务模版
    传入示例：delete_service_template_name('ap1',['g1','g2','g0','hsh'])
    """
    dut = connect(device_name)
    
    dut.send(f"""
                    system-view
                    wlan ap {apname}
                """)  
         
    for i in range(len(ser_name)):

        dut.send(f"""
                    radio 1
                    undo service-template {ser_name[i]}
                    Y
                    radio 2
                    undo service-template {ser_name[i]}
                    Y
                    radio 3
                    undo service-template {ser_name[i]}
                    Y
                """)
        
def add_service_template_name(device_name,apname,ser_name):
    """
    按名字绑定服务模版
    传入示例：add_service_template_name('ap1',['g1','g2','g0','hsh'])
    """
    dut = connect(device_name)
    dut.send(f"""
                    system-view
                    wlan ap {apname}
                """)  
    for i in range(len(ser_name)):
        dut.send(f"""
                    radio 1
                    service-template {ser_name[i]}
                    radio 2
                    service-template {ser_name[i]}
                    radio 3
                    service-template {ser_name[i]}
                """)


       
if __name__ == '__main__':
    pass
    # 创建服务模版
    # set_service_template("qx1240",13)
    #radio 下绑定
    # set_radio_service_template(10)
    # #云AP radio 下绑定
    
    # cloud_ap_radio_service_template()
    # #云AP radio 下解绑定
    # cloud_ap_radio_service_template_undo()
    # #radio 下解绑定
    # ap_radio_service_template_undo(14)
    # #删除服务模版
    # delete_service_template(15)
    # while True:
        
    # add_service_template_name('qx1240','ap1',['wpa3-h2e','g0','g1','g2','wpa3-hnp','g3','g4','g5','g6','g7','g8','g9','g10','g11','g12'])
    # delete_service_template_name('qx1240','ap1',['wpa3-h2e','g0','g1','g2','wpa3-hnp','g3','g4','g5','g6','g7','g8','g9','g10','g11','g12'])
    #     connect_to_wifi('Z5Y5KZY9LZRS69JF',"00*h2e-V9","123123123")
    #     time.sleep(10)
        # delete_service_template_name('ap1',['wpa3-h2e','g1','g2','g0','g11','g3','g4','g5','g6','g7','g8','g9','g10'])
    
    # delete_service_template_name('ap1',['g2','g0','hsh','g3','g4','g5','g6','g7','g8','g9','g10'])
    # add_service_template_name(ap1',['g1','g2','g0','hsh','g3','g4','g5','g6','g7','g8','g9','g10'])
    # connect_to_wifi('Z5Y5KZY9LZRS69JF',"00*h2e-V9","123123123")



