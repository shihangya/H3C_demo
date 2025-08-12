import os
import time
import threading
import re
import uiautomator2 as u2
import subprocess
import time
# from asyncio.tasks import sleep
def devices_serial_id():
    device_list=[]
    try:
        view=os.popen("adb devices").readlines()
        for serial in view[1:]:
            if "device" in serial:
                device_list.append(serial.split("\t")[0])
        if device_list:
            return device_list
        else:
            return False
    except Exception as e:
        print(e)
        return False

    
def get_wlan0(serial_id,view="IP"):
    print(serial_id,view)
    result="False"
    data=os.popen("adb -s "+ str(serial_id) +" shell ip -4 addr").read()
    time.sleep(1)
    try:
        data_complie=re.compile('wlan0(.*?)wlan0',re.S)
        demo=re.findall(data_complie,data)[0]
        print(demo)
        mask_complie1 = re.compile('/(.*?) brd',re.S)
        mask = re.findall(mask_complie1,demo)[0]
        print(mask)
        if view=="IP":
            if mask == '24' :
                IP_complie = re.compile('inet(.*?)/24',re.S)
                result = re.findall(IP_complie,demo)[0].rstrip()
            elif mask == '16' :
                IP_complie = re.compile('inet(.*?)/16',re.S)
                result = re.findall(IP_complie,demo)[0].rstrip()
            print(result)
        else :
            result="False"
    except Exception as e:
        result=str(serial_id)+" False: " + str(e)
    finally:
        time.sleep(1)
        return result

def get_macaddress(serial_id,pcsta_mac):
    if  serial_id == "PC_STA": 
        result=pcsta_mac
    else:
        try:
            data=os.popen("adb -s "+ str(serial_id) +" shell ip address show wlan0").read()
            macaddress=data.split("link/ether")[1].split("brd")[0].lstrip().rstrip()
            data=macaddress.split(":")
            result=data[0]+ data[1]+"-"+data[2]+data[3]+"-"+data[4]+data[5]
        except Exception as e:
            print(e)
            result=str(e)
    return result


def adb_join_wifi(serial_id,ssid,auth_mode=None,username=None,password=None,static_ip=None):
    print(serial_id,ssid,auth_mode,username,password,static_ip)
    os.system("adb -s "+ str(serial_id) +" shell svc wifi enable")
    time.sleep(1)
    os.system("adb -s "+ str(serial_id) +" shell am force-stop com.steinwurf.adbjoinwifi")
    time.sleep(1)
#     os.system("adb -s "+ str(serial_id) +" shell am start -n com.steinwurf.adbjoinwifi/.MainActivity --esn remove")
#     time.sleep(1)
    return_view="False"
    try:
        command_demo = "adb -s "+ str(serial_id) +" shell am start -n com.steinwurf.adbjoinwifi/.MainActivity --esn connect -e ssid "
        Static_IP = " -e ip "+ str(static_ip)
        if auth_mode == None or auth_mode == "MAC":
            adb_command=command_demo + str(ssid)
            print(adb_command)
        elif auth_mode == "WEP":
            adb_command=command_demo +str(ssid) + " -e password_type WEP "+"-e password " + str(password)
            print(adb_command)
        elif auth_mode == "WPA2" or auth_mode == "WPA" or auth_mode == "RSN":
            adb_command=command_demo + str(ssid) + " -e password_type WPA "+"-e password " + str(password)
            print(adb_command)
        elif auth_mode =="PEAP":
            adb_command = command_demo + str(ssid) + " -e password_type PEAP "+"-e username " + str(username) +" -e password " + str(password)
            print(adb_command)
        else:
            print("Please check auth_mode")
            adb_command=None
            return_view="auth_mode Error"
        if adb_command:
            if static_ip:
                os.system(adb_command + Static_IP)
                print(adb_command,Static_IP)
            else:
                os.system(adb_command)
    except Exception as e:
        print(e)
        return_view=str(serial_id)+" False: " + str(e)
    finally:
        for i in range(10):
            time.sleep(5)
            a=get_wlan0(serial_id,view="IP")
            print(a)
            if a.count(".")==3:
                print(str(serial_id)+' ip: '+ a +'\n')
                return_view="True"
                os.system("adb -s "+ str(serial_id) +" shell am force-stop com.steinwurf.adbjoinwifi")
#                 os.system("adb -s "+ str(serial_id) +" shell am start -n com.steinwurf.adbjoinwifi/.MainActivity --esn remove")
                break
            else :
                return_view="False"
        time.sleep(5)
        return return_view 

def adb_open_wifi(serial_id,ssid,auth_mode=None,username=None,password=None,static_ip=None):
    print(serial_id,ssid,auth_mode,username,password,static_ip)
    return_view="True"
    try:
        #os.system("adb -s "+ str(serial_id) +" shell svc wifi disable")
        #time.sleep(1)
        os.system("adb -s "+ str(serial_id) +" shell svc wifi enable")
        time.sleep(1)
    finally:
        os.system("adb -s "+ str(serial_id) +" shell am force-stop com.steinwurf.adbjoinwifi")
        return return_view
    
def adb_close_wifi(serial_id,ssid,auth_mode=None,username=None,password=None,static_ip=None):
    print(serial_id,ssid,auth_mode,username,password,static_ip)
    return_view="True"
    try:
        os.system("adb -s "+ str(serial_id) +" shell svc wifi disable")
        time.sleep(1)
    finally:
        os.system("adb -s "+ str(serial_id) +" shell am force-stop com.steinwurf.adbjoinwifi")
        return return_view
    


def adb_disconnect(serial_id):
    os.system("adb -s "+ str(serial_id) +" shell am force-stop com.steinwurf.adbjoinwifi")
    time.sleep(1)
    os.system("adb -s "+ str(serial_id) +" shell am start -n com.steinwurf.adbjoinwifi/.MainActivity --esn remove")
    time.sleep(1)
    IP=get_wlan0(serial_id)
    if "False" in IP:
        result="True"
    else:
        result="False"
    return result

    
def portal_online(serial_id,url,username,password):
    import uiautomator2 as u2
    judge=False
    try:
        os.system("adb -s "+ str(serial_id) +" shell input keyevent 3")
        time.sleep(2)
        adb_command="adb -s "+ str(serial_id) +" shell am start -a android.intent.action.VIEW -d "+str(url)
        os.system(adb_command)
        time.sleep(2)
        d = u2.connect(str(serial_id))
        time.sleep(1)
        d.uiautomator.start()
        time.sleep(1)
        if d(resourceId="id_userName").wait(timeout=10.0):
            d(resourceId="id_userName").set_text(str(username))
            time.sleep(4)
            judge=True
        if judge:
            d(resourceId="id_userPwd").set_text(str(password))
            time.sleep(4)
            d(text=u"上线").click()
            time.sleep(3)
            view = "True"
        else:
            print(str(serial_id)+" Interface elements have changed,please modify the code")
            view =str(serial_id)+" False: Interface elements have changed,please modify the code"
    except Exception as e:
        print(str(serial_id)+" False: " + str(e))
        view=str(serial_id)+" False: " + str(e)
    finally:
        os.system("adb -s "+ str(serial_id) +" shell input keyevent 3")
        return view
#portal_online("4534364759583098","9.0.0.250:8080/portal","portal-hxl","portal-hxl")               

def portal_offline(serial_id,url,username,password):
    import uiautomator2 as u2
    judge=False
    try:
        os.system("adb -s "+ str(serial_id) +" shell input keyevent 3")
        time.sleep(2)
        adb_command="adb -s "+ str(serial_id) +" shell am start -a android.intent.action.VIEW -d "+str(url)
        os.system(adb_command)
        d = u2.connect(str(serial_id))
        if d(resourceId="id_userName").wait(timeout=10.0):
            d(resourceId="id_userName").set_text(str(username))
            judge=True
            time.sleep(2)
        if judge:
            d(resourceId="id_userPwd").set_text(str(password))
            time.sleep(2)
            d(text=u"下线").click()
            view = "True"
        else:
            print(str(serial_id)+" Interface elements have changed,please modify the code")
            view =str(serial_id)+" False: Interface elements have changed,please modify the code"
    except Exception as e:
        print(str(serial_id)+" False: " + str(e))
        view=str(serial_id)+" False: " + str(e)
    finally:
        os.system("adb -s "+ str(serial_id) +" shell input keyevent 3")
        return view
    
###################################       单用户             ###############################################
    
#######################################################################################################
#功   能：当PC usb连接仅一个手机时,控制手机接入wifi
#原   型：single_connect
#类   型：def
#输   入：
#         ssid      -  SSID
#         auth_mode -  认证方式     [auth_mode= None | WEP | WPA | WPA2 |PEAP]
#         username  -  接入dot1x服务时，需要输入的账号
#         password  -  密码
#输   出：运行成功返回"True"
#举   例：连接clear服务
#     single_connect("00H3C")
#作   者：fuyong fys1736 2019.12.10
##########################################################################################################
def single_connect(ssid,auth_mode=None,username=None,password=None,static_ip=None):
    data=devices_serial_id()
    if len(data)==1:
        result=adb_join_wifi(data[0],ssid,auth_mode,username,password,static_ip)
        return result
    else:
        result="Please check the usb-connected STA"
        return result

#######################################################################################################
#功   能：当PC usb连接仅一个手机时,控制连接wifi服务的手机下线
#原   型：single_disconnect
#类   型：def
#输   入：
# 
#输   出：运行成功返回"True"
#举   例：控制手机下线
#     single_disconnect()
#作   者：fuyong fys1736 2019.12.10
##########################################################################################################
def single_disconnect():
    data=devices_serial_id()
    if len(data)==1:
        result=adb_disconnect(data[0])
        return result
    else:
        result="Please check the usb-connected STA"
        print(result)
        return result

#######################################################################################################
#功   能：当手机接入wifi服务时,获取指定接入手机的IP
#原   型：single_get_IP
#类   型：def
#输   入：serail_id  -   默认为None，此时:PC仅usb连接一个手机
#                        其余情况都需要输入serial_id实参
# 
#输   出：运行成功返回IP地址
#举   例：PC usb仅连接一个手机，获取接入dot1x PEAP + CCMP wifi的手机的IP
#     single_get_IP()
#作   者：fuyong fys1736 2019.12.10
##########################################################################################################
def single_get_IP(serail_id=None):
    if serail_id:
        data=serail_id
    else:
        data=devices_serial_id()[0]
    if len(data)==1:
        result=get_wlan0(data)
        return result
    else:
        result="Please check the usb-connected STA"
        print(result)
        return result
#######################################################################################################
#功   能：当PC usb连接仅一个手机时,手机进行portal认证上线
#原   型：single_portal_online
#类   型：def
#输   入：
#         url        -    认证url，可验证重定向
#         username   -    认证帐号
#         password   -    认证密码
# 
#输   出：运行成功返回"True"
#举   例：进行clear服务的portal认证上线
#     single_portal_online("http://1.1.1.1","portal-fy","portal-fy")
#作   者：fuyong fys1736 2019.12.10
#########################################################################################################
def single_portal_online(url,username,password):
    data=devices_serial_id()
    if len(data)==1:
        result=portal_online(data[0],url,username,password)
        return result
    else:
        result="Please check the usb-connected STA"
        print(result)
        return result
   
#######################################################################################################
#功   能：当PC usb连接仅一个手机时,手机进行portal认证下线
#原   型：single_get_IP
#类   型：def
#输   入：
#         url       -     认证url，必须输入完整的认证地址，看举例
#         username  -     认证帐号
#         password  -     认证密码
#输   出：运行成功返回"True"
#举   例：进行clear服务的portal认证下线
#     single_portal_offline("http://9.0.0.250:8080/portal","portal-fy","portal-fy")
#作   者：fuyong fys1736 2019.12.10
##########################################################################################################
def single_portal_offline(url,username,password):
    data=devices_serial_id()
    if len(data)==1:
        result=portal_offline(data[0],url,username,password)
        return result
    else:
        result="Please check the usb-connected STA"
        print(result)
        return result
     
    
#######################################################################################################
#功   能：当PC usb连接多个手机时,控制指定的手机接入wifi
#原   型：multi_connect
#类   型：def
#输   入：
#         serial_id_list   -   可识别手机的serial id 组成的列表
#         ssid      -  SSID
#         auth_mode -  认证方式     [auth_mode= None | WEP | WPA | WPA2 |PEAP]
#         username  -  接入dot1x服务时，需要输入的账号
#         password  -  密码
#输   出：运行成功返回"True"
#举   例：当PC usb连接多个手机时,指定两款手机接入clear服务
#     multi_connect(['f965208e','9eb99ebb'],"00H3C")
#作   者：fuyong fys1736 2019.12.10
##########################################################################################################
def multi_connect(serial_id_list,ssid,auth_mode=None,username=None,password=None,static_ip=None):
    pid_list=[]
    result="True"
    try:
        if len(serial_id_list) >=  1:
            for i in serial_id_list:
                t=threading.Thread(target=adb_join_wifi,args=(i,ssid,auth_mode,username,password,static_ip))
                pid_list.append(t)
            for j in pid_list:
                j.start()
            for j in pid_list:
                j.join()
        else:
            result="Please check serial_id_list"
            print(result)
    except Exception as e:
        print(e)
        result="False: " + str(e)
    finally:
        return result

#######################################################################################################
#功   能：当PC usb连接多个手机时,控制指定手机下线
#原   型：multi_disconnect
#类   型：def
#输   入：
#         serial_id_list      可识别手机的serial id 组成的列表
#输   出：运行成功返回"True"
#举   例：控制指定的两款手机下线
#     multi_disconnect(['f965208e','9eb99ebb'])
#作   者：fuyong fys1736 2019.12.10
##########################################################################################################
def multi_disconnect(serial_id_list):
    pid_list=[]
    result="True"
    try:
        if len(serial_id_list) >=  1:
            for i in serial_id_list:
                t=threading.Thread(target=adb_disconnect,args=(i,))
                pid_list.append(t)
            for j in pid_list:
                j.start()
            for j in pid_list:
                j.join()
        else:
            result="Please check serial_id_list"
            print(result)
    except Exception as e:
        print(e)
        result="False: " + str(e)
    finally:
        return result

    
#######################################################################################################
#功   能：当PC usb连接多个手机时,控制指定手机portal认证上线
#原   型：multi_portal_online
#类   型：def
#输   入：
#         serial_id_list 可识别手机的serial id 组成的列表
#         url            认证url，可验证重定向
#         username       认证帐号
#         password       认证密码
# 
#输   出：运行成功返回True
#举   例：控制指定手机进行portal认证上线
#     multi_portal_online(['4534364759583098','R28M31YKZVA','f965208e','9eb99ebb'],"http://1.1.1.1","portal-fy","portal-fy")
#作   者：fuyong fys1736 2019.12.10
#########################################################################################################
def multi_portal_online(serial_id_list,url,username,password):
    pid_list=[]
    result="True"
    try:
        if len(serial_id_list) >=  1:
            for i in serial_id_list:
                t=threading.Thread(target=portal_online,args=(i,url,username,password))
                pid_list.append(t)
            for j in pid_list:
                j.start()
            for j in pid_list:
                j.join()
        else:
            result="Please check serial_id_list"
            print(result)
    except Exception as e:
        print(e)
        result="False: " + str(e)
    finally:
        return result

#######################################################################################################
#功   能：当PC usb连接多个手机时,控制指定手机portal认证下线
#原   型：multi_portal_offline
#类   型：def
#输   入：
#         serial_id_list 可识别手机的serial id 组成的列表
#         url            认证url，必须输入完整的认证地址，看举例
#         username       认证帐号
#         password       认证密码
# 
#输   出：运行成功返回True
#举   例：控制指定手机进行的portal认证下线
#     multi_portal_offline(['4534364759583098','R28M31YKZVA','f965208e','9eb99ebb'],"http://9.0.0.250:8080/portal","portal-fy","portal-fy")
#作   者：fuyong fys1736 2019.12.10
#########################################################################################################
def multi_portal_offline(serial_id_list,url,username,password):
    pid_list=[]
    result="True"
    try:
        if len(serial_id_list) >=  1:
            for i in serial_id_list:
                t=threading.Thread(target=portal_online,args=(i,url,username,password))
                pid_list.append(t)
            for j in pid_list:
                j.start()
            for j in pid_list:
                j.join()
        else:
            result="Please check serial_id_list"
            print(result)
    except Exception as e:
        print(e)
        result="False: " + str(e)
    finally:
        return result

#######################################################################################################
#功   能：使PC usb连接的所有手机接入wifi
#原   型：multi_connect
#类   型：def
#输   入：
#         ssid      -  SSID
#         auth_mode -  认证方式     [auth_mode= None | WEP | WPA | WPA2 |PEAP]
#         username  -  接入dot1x服务时，需要输入的账号
#         password  -  密码
#输   出：运行成功返回"True"
#输   出：运行成功返回"True"
#举   例：使PC usb连接的所有手机接入clear服务
#     multi_all("00H3C")
#作   者：fuyong fys1736 2019.12.10
##########################################################################################################
def multi_all(ssid,auth_mode=None,username=None,password=None,static_ip=None):
    pid_list=[]
    serial_id_list=devices_serial_id()
    result="True"
    try:
        if len(serial_id_list) >=  1:
            for i in serial_id_list:
                t=threading.Thread(target=adb_join_wifi,args=(i,ssid,auth_mode,username,password,static_ip))
                pid_list.append(t)
            for j in pid_list:
                j.start()
            for j in pid_list:
                j.join()
        else:
            result="Please check serial_id_list"
            print(result)
    except Exception as e:
        print(e)
        result="False: " + str(e)
    finally:
        return result

#######################################################################################################
#功   能：使PC usb连接的所有手机断开wifi连接
#原   型：multi_all_disconnect
#类   型：def
#输   入：
#         
#输   出：运行成功返回"True"
#举   例：使PC usb连接的所有手机断开wifi连接
#     multi_all_disconnect()
#作   者：fuyong fys1736 2019.12.10
##########################################################################################################
def multi_all_disconnect():
    pid_list=[]
    serial_id_list=devices_serial_id()
    result="True"
    try:
        if len(serial_id_list) >=  1:
            for i in serial_id_list:
                t=threading.Thread(target=adb_disconnect,args=(i,))
                pid_list.append(t)
            for j in pid_list:
                j.start()
            for j in pid_list:
                j.join()
        else:
            result="Please check serial_id_list"
            print(result)
    except Exception as e:
        print(e)
        result="False: " + str(e)
    finally:
        return result
    
#######################################################################################################
#功   能：控制PC usb连接的所有手机portal认证上线
#原   型：multi_all_portal_online
#类   型：def
#输   入：
#         url            认证url，可验证重定向
#         username       认证帐号
#         password       认证密码
# 
#输   出：运行成功返回True
#举   例：控制PC usb连接的所有手机portal认证上线
#     multi_all_portal_online("http://1.1.1.1","portal-fy","portal-fy")
#作   者：fuyong fys1736 2019.12.10
#########################################################################################################
def multi_all_portal_online(url,username,password):
    pid_list=[]
    serial_id_list=devices_serial_id()
    result="True"
    try:
        if len(serial_id_list) >=  1:
            for i in serial_id_list:
                t=threading.Thread(target=portal_online,args=(i,url,username,password))
                pid_list.append(t)
            for j in pid_list:
                j.start()
            for j in pid_list:
                j.join()
        else:
            result="Please check serial_id_list"
            print(result)
    except Exception as e:
        print(e)
        result="False: " + str(e)
    finally:
        return result    
   
#######################################################################################################
#功   能：控制PC usb连接的所有手机portal认证下线
#原   型：multi_all_portal_offline
#类   型：def
#输   入：
#         url            认证url，必须输入完整的认证地址，看举例
#         username       认证帐号
#         password       认证密码
# 
#输   出：运行成功返回True
#举   例：控制PC usb连接的所有手机portal认证下线
#     multi_all_portal_offline("http://9.0.0.250:8080/portal","portal-fy","portal-fy")
#作   者：fuyong fys1736 2019.12.10
#########################################################################################################
def multi_all_portal_offline(url,username,password):
    pid_list=[]
    serial_id_list=devices_serial_id()
    print(serial_id_list)
    result="True"
    try:
        if len(serial_id_list) >=  1:
            for i in serial_id_list:
                t=threading.Thread(target=portal_offline,args=(i,url,username,password))
                pid_list.append(t)
            for j in pid_list:
                j.start()
            for j in pid_list:
                j.join()
        else:
            result="Please check serial_id_list"
            print(result)
    except Exception as e:
        print(e)
        result="False: " + str(e)
    finally:
        return result
   
#######################################################################################################
#功   能：PC usb仅接入一个手机时，控制手机ping一个指定的地址
#原   型：single_ping
#类   型：def
#输   入：
#         ip             要ping的设备的IP
#         Count          ping的次数，默认4次
#         serial_id      指定手机的serial_id,默认None即PC仅接一个手机时。
#输   出：运行成功返回“True”
#举   例：指定手机ping 9.3.0.3且ping10次
#         STA_ping('9.3.0.3',10)
#作   者：fuyong fys1736 2019.12.16
#########################################################################################################
def single_ping(ip,Count=4,serial_id=None):
    if serial_id:
        serial=serial_id
    else:
        serial=devices_serial_id()[0]
    cmd="adb -s "+ str(serial) +" shell ping -c "+str(Count)+" %s" %ip
    view=os.popen(cmd).read()
    amount=view.count("ttl")
    print(str(serial)+" ping: TTL="+str(amount))
    if amount >=1:
        return "True"
    else:
        return "False"

#######################################################################################################
#功   能：PC usb仅接入一个手机时，控制手机ping一个指定的地址
#原   型：multi_ping
#类   型：def
#输   入：
#         serial_id_list 可识别手机的serial id 组成的列表
#         ip             要ping的设备的IP
#         Count          ping的次数，默认4次
#输   出：运行成功返回“True”
#举   例：指定手机ping 9.3.0.3且ping4次
#         multi_ping(['R28M31YKZVA'],'9.3.0.3')
#作   者：fuyong fys1736 2019.12.16
#########################################################################################################
def multi_ping(serial_id_list,ip,Count=4):
    pid_list=[]
    result="True"
    try:
        if len(serial_id_list) >=  1:
            for i in serial_id_list:
                t=threading.Thread(target=single_ping,args=(ip,Count,i))
                pid_list.append(t)
            for j in pid_list:
                j.start()
            for j in pid_list:
                j.join()
        else:
            result="Please check serial_id_list"
            print(result)
    except Exception as e:
        print(e)
        result="False: " + str(e)
    finally:
        return result

#######################################################################################################
#功   能：使PC usb连接的所有手机ping
#原   型：multi_all_ping
#类   型：def
#输   入：
#         ip             要ping的设备的IP
#         Count          ping的次数，默认4次
#输   出：运行成功返回"True"
#输   出：运行成功返回"True"
#举   例：使PC usb连接的所有手机ping 9.3.0.3且ping10次
#         STA_ping('9.3.0.3',10)
#作   者：fuyong fys1736 2019.12.16
##########################################################################################################
def multi_all_ping(ip,Count=4):
    pid_list=[]
    serial_id_list=devices_serial_id()
    result="True"
    try:
        if len(serial_id_list) >=  1:
            for i in serial_id_list:
                t=threading.Thread(target=single_ping,args=(ip,Count,i))
                pid_list.append(t)
            for j in pid_list:
                j.start()
            for j in pid_list:
                j.join()
        else:
            result="Please check serial_id_list"
            print(result)
    except Exception as e:
        print(e)
        result="False: " + str(e)
    finally:
        return result
    
def control_endpoint(serial_id,state):
    judge=1
    if state=="open":
        cmd="adb -s "+ str(serial_id) +" shell am start -n com.ixia.ixchariot/com.ixia.ixchariot.Endpoint"
        cmd1="adb -s "+ str(serial_id) +" shell am start -n com.ixia.ixchariot/com.ixia.ixchariot.EndpointActivity"
    elif state=="close":
        cmd="adb -s "+ str(serial_id) +" shell am force-stop com.ixia.ixchariot"
        cmd1="adb -s "+ str(serial_id) +" shell am force-stop com.ixia.ixchariot"               
    else:
        print("state 参数传错")
        judge=0
    if judge:
        result=os.popen(cmd).read()
        result1=os.popen(cmd1).read()        
        print(result+result1)


def speedtest_andriod(serial_id,url):
    import uiautomator2 as u2
    speedtest_rusult=[]
    try:
        os.system("adb -s "+ str(serial_id) +" shell input keyevent 3")         ##返回桌面
        time.sleep(2)
        adb_command="adb -s "+ str(serial_id) +" shell am start -a android.intent.action.VIEW -d "+str(url)  ##打开默认浏览器，访问url
        os.system(adb_command)
        time.sleep(5)
        d = u2.connect(str(serial_id))
        time.sleep(5)          
        if d(resourceId="startStopBtn").wait(timeout=10.0):
            a=d(resourceId="startStopBtn").exists()
            print(a)
            d(resourceId="startStopBtn").click()
            time.sleep(150)
            download_speed=d(resourceId="dlText").get_text()
            upload_speed=d(resourceId="ulText").get_text()
            ping=d(resourceId="pingText").get_text()
            jit=d(resourceId="jitText").get_text()
            speedtest_rusult.extend([download_speed,upload_speed,ping,jit])                        
            view=speedtest_rusult
            print(speedtest_rusult)

        else:
            print(str(serial_id)+" Interface elements have changed,please modify the code")
            a =str(serial_id)+" False: Interface elements have changed,please modify the code"
            view = ['False',a]
    except Exception as e:
        print(str(serial_id)+" False: " + str(e))
        a=str(serial_id)+" False: " + str(e)
        view = ['False',a]
    finally:
        os.system("adb -s "+ str(serial_id) +" shell input keyevent 3")
        return view 
    
def get_wlan0_android14(udid, view="IP"):
    """
        功能：
            获取某个手机的ip地址或者ipv6地址
        参数：
            udid：手机的udid
            view="IP" : 默认为IP地址，可选传参IPv6
        返回值：
            返回手机的ip/ipv6地址
        举例：
    get_wlan0('2eb38cdb')
        作者/日期：

    """
    #     print(udid,view)
    result = "False"
    if view == "IP":
        adb_command = "adb -s " + str(udid) + " shell ip -4 addr"
    else:
        adb_command = "adb -s " + str(udid) + " shell ip -6 addr"
    data = os.popen(adb_command).read()
    time.sleep(1)
    if data:
        if "wlan0" in data:
            if view == "IP":
                try:
                    #                     print(data)
                    data_complie = re.compile('wlan0(.*?)wlan0', re.S)
                    demo = re.findall(data_complie, data)[0]
                    #                     print(demo)
                    mask_complie1 = re.compile('/(.*?) brd', re.S)
                    mask = re.findall(mask_complie1, demo)[0]
                    #                     print(mask)
                    if mask == '24':
                        IP_complie = re.compile('inet(.*?)/24', re.S)
                        result = re.findall(IP_complie, demo)[0].rstrip()
                    elif mask == '16':
                        IP_complie = re.compile('inet(.*?)/16', re.S)
                        result = re.findall(IP_complie, demo)[0].rstrip()
                    print(result)
                except Exception as e:
                    result = str(udid) + " False: " + str(e)
            else:
                try:
                    result = re.findall("inet6 (.*) scope global", data)[0]
                    print(result)
                except Exception as e:
                    result = str(udid) + " False: " + str(e)
        else:
            print("{adb_command}\n返回值  {data}\n没有IP地址")
            result = "False"
    else:
        print("{adb_command}\n没有返回值 ")
        result = "False"
    return result


def get_mobile_phone_brand_android14(udid):
    """
        功能：
            获取手机的型号
        参数：
            udid：手机的udid
        返回值：
            设置为手机型号：str
        举例：
    get_mobile_phone_brand('2eb38cdb')
        作者/日期：
    """
    cmd = "adb -s {udid} shell getprop ro.product.brand"
    mobile_phone_brand = os.popen(cmd).read()
    mobile_phone_brand = re.sub("\s", "", mobile_phone_brand)
    print("----{mobile_phone_brand}----")
    return mobile_phone_brand


def click_wlan_connect_wpa3_enterprise_radmi(udid, ssid, ca_name, localhost, user, eap='TLS'):
    """
       功能：
           1.手机通过点击WLAN，连接WPA3企业级服务模板
           2.点击SSID后，选择证书，输入localhost,输入user用户名，点击确定连接
           3.该接口，受手机型号限制，
           4.已经兼容了HONOR
       参数：
           udid：手机的udid
           ssid：手机所连接的无线服务
           ca_name：证书名称（安装证书时，给证书的命名，此处需要选择安装的证书名）
           localhost：域名：一般IMC上填写的为localhost
           user：IMC上用户名
       返回值：
           点击成功返回'True',失败返回'False'
       举例：
   click_wlan_connect_OWE('2eb38cdb','ssid_1','client',localhost='localhost',user='user')
       作者/日期：
       duanwnexing/2023/10/17    zhengchao--20240528 修改兼容红米K70P
   """


    result = 'False'
    mobile_phone_brand = get_mobile_phone_brand_android14(udid)
    activity = ".Settings"
    if mobile_phone_brand == "HONOR":
        activity = ".HWSettings"
        os.system("adb -s " + str(udid) + " shell input keyevent 3")
    try:
        d = u2.connect(str(udid))
        time.sleep(1)
        d.uiautomator.start()
        time.sleep(1)
        # 切换成 ui2 的输入法，这里会隐藏掉系统原本的输入法 , 默认是使用系统输入法
        # 当传入 False 时会使用系统默认输入法，默认为 Fasle
        d.set_fastinput_ime(True)
        # 查看当前输入法
        print(d.current_ime())
        print("False 时会使用系统默认输入法'")
    # 打开设置
        try:
            d.app_start("com.android.settings", activity, stop=True)
        except:
            d.app_start("com.android.settings", stop=True)
        time.sleep(3)
    # 点击WLAN
        d(resourceId="android:id/title", text="WLAN").click()
        time.sleep(5)
    # 查找需连接的WiFi，并以此作为是否继续执行的依据
        count = 0
        while count <= 5:
            if d(resourceId="android:id/title", text=ssid).exists():
                d(resourceId="android:id/title", text=ssid).click()
                time.sleep(5)
                d.xpath('//*[@resource-id="com.android.settings:id/method"]/android.widget.LinearLayout[1]/android.widget.ImageView[1]').click()
                d(resourceId="android:id/text1", text=eap).click()
                d.xpath('//*[@resource-id="com.android.settings:id/ca_cert"]/android.widget.LinearLayout[1]/android.widget.ImageView[1]').click()
                d(resourceId="android:id/text1", text=ca_name).click()
                time.sleep(3)
                d(resourceId="com.android.settings:id/domain").click()
                d.send_keys(localhost, clear=True)
                time.sleep(2)
#                d.xpath('//*[@resource-id="com.android.settings:id/user_cert"]/android.widget.LinearLayout[1]/android.widget.ImageView[1]').click()
#                d(resourceId="android:id/text1", text=ca_name).click()
                time.sleep(2)
                d(resourceId="com.android.settings:id/identity").click()
                d.send_keys(user, clear=True)
                time.sleep(2)
                d(resourceId="android:id/button1").click()
                time.sleep(10)
                a = get_wlan0_android14(udid)
                print(a)
                if a.count(".") == 3:
                    print(str(udid) + ' ip: ' + a + '\n')
                    result = "True"
                elif a.count(":") >= 2:
                    print(str(udid) + ' ipv6: ' + a + '\n')
                    result = "True"
                else:
                    result = "获取IP地址失败：False"
                break
            else:
                print("手机{udid}未搜到{ssid}的WiFi，下滑页面继续查找")
                d.swipe(394, 1600, 394, 600, steps=20)
                count += 1

    except Exception as e:
        print("手机设连接wifi失败 :{e}")
        result = 'False'
    finally:
        d.app_stop("com.android.settings")
        return result
def click_wlan_connect_1x_peap_radmi(udid,ssid,user,password,eap='eap'):
    """
       功能：
           1.手机通过点击WLAN，连接1x eap-peap认证
           2.点击SSID后，输入user用户名和密码，点击链接
           3.该接口，受手机型号限制，
           4.已经兼容了HONOR
       参数：
           udid：手机的udid
           ssid：手机所连接的无线服务
           user：1x认证用户用户名
           password：1x认证用户密码
       返回值：
           点击成功返回'True',失败返回'False'
       举例：
   click_wlan_connect_OWE('2eb38cdb','ssid_1',user='user',password='password',eap='eap')
       作者/日期：
       /2023/10/17      zhengchao--20240528 修改兼容红米K70P
   """


    result = 'False'
    mobile_phone_brand = get_mobile_phone_brand_android14(udid)
    activity = ".Settings"
    if mobile_phone_brand == "HONOR":
        activity = ".HWSettings"
        os.system("adb -s " + str(udid) + " shell input keyevent 3")
    try:
        d = u2.connect(str(udid))
        time.sleep(1)
        d.uiautomator.start()
        time.sleep(1)
        # 切换成 ui2 的输入法，这里会隐藏掉系统原本的输入法 , 默认是使用系统输入法
        # 当传入 False 时会使用系统默认输入法，默认为 Fasle
        d.set_fastinput_ime(True)
        # 查看当前输入法
        print(d.current_ime())
        print("False 时会使用系统默认输入法'")
    # 打开设置
        try:
            d.app_start("com.android.settings", activity, stop=True)
        except:
            d.app_start("com.android.settings", stop=True)
        time.sleep(3)
    # 点击WLAN
        d(resourceId="android:id/title", text="WLAN").click()
        time.sleep(5)
    # 查找需连接的WiFi，并以此作为是否继续执行的依据
        count = 0
        while count <= 5:
            if d(resourceId="android:id/title", text=ssid).exists():
                d(resourceId="android:id/title", text=ssid).click()
                time.sleep(5)
                if d(resourceId="android:id/text1", text="使用系统证书").exists():
                    d(resourceId="android:id/text1", text="使用系统证书").click()
                    time.sleep(1)
                    d(resourceId="android:id/text1", text="不验证").click()
                    time.sleep(1)                    
                    d(resourceId="com.android.settings:id/identity").click()
                    d.send_keys(user, clear=True)
                    time.sleep(2)
                    d(resourceId="com.android.settings:id/password").click()
                    d.send_keys(password, clear=True)
                    time.sleep(2)
                    d(resourceId="android:id/button1").click()
                    time.sleep(10)
                    print('进入第一分支上线点击成功：')
                    result = "True"
                else:
                    d(resourceId="com.android.settings:id/identity").click()
                    d.send_keys(user, clear=True)
                    d(resourceId="com.android.settings:id/password").click()
                    d.send_keys(password, clear=True)
                    time.sleep(2)
                    d(resourceId="android:id/button1").click()
                    time.sleep(2)
                    print('进入第二分支，上线点击成功~')
                    result = "True"
                a = get_wlan0_android14(udid)
                if a.count(".") == 3:
                    print(str(udid) + ' ip: ' + a + '\n')
                    result = "True"
                elif a.count(":") >= 2:
                    print(str(udid) + ' ipv6: ' + a + '\n')
                    result = "True"
                else:
                    result = "获取IP地址失败：False"
                break
            else:
                print("手机{udid}未搜到{ssid}的WiFi，下滑页面继续查找")
                d.swipe(394, 1600, 394, 600, steps=20)
                count += 1

    except Exception as e:
        print("手机设连接wifi失败 :{e}")
        result = 'False'
    finally:
        d.app_stop("com.android.settings")
        return result
    
def click_wlan_connect_wpa3_rsn_ccmp_radmi(udid, ssid, password):
    print('udid:',udid,'ssid:',ssid,'password:',password)
    """
       功能：
           1.手机通过点击WLAN，连接WPA3企业级服务模板
           2.点击SSID后，输入rsn+ccmp的密码关联服务
           3.该接口，受手机型号限制，
           4.已经兼容了HONOR
       参数：
           udid：手机的udid
           ssid：手机所连接的无线服务
           password：1x认证用户密码
       返回值：
           点击成功返回'True',失败返回'False'
       举例：
   click_wlan_connect_wpa3_rsn_ccmp_radmi('2eb38cdb','ssid_1',password='password')
       作者/日期：
       duanwnexing/2023/10/17    zhengchao--20240528 修改兼容红米K70P
   """


    result = 'False'
    mobile_phone_brand = get_mobile_phone_brand_android14(udid)
    activity = ".Settings"
    if mobile_phone_brand == "HONOR":
        activity = ".HWSettings"
        os.system("adb -s " + str(udid) + " shell input keyevent 3")
    try:
        d = u2.connect(str(udid))
        time.sleep(1)
        d.uiautomator.start()
        time.sleep(1)
        # 切换成 ui2 的输入法，这里会隐藏掉系统原本的输入法 , 默认是使用系统输入法
        # 当传入 False 时会使用系统默认输入法，默认为 Fasle
        d.set_fastinput_ime(True)
        # 查看当前输入法
        print(d.current_ime())
        print("False 时会使用系统默认输入法'")
    # 打开设置
        try:
            d.app_start("com.android.settings", activity, stop=True)
        except:
            d.app_start("com.android.settings", stop=True)
        time.sleep(3)
    # 点击WLAN
        d(resourceId="android:id/title", text="WLAN").click()
        time.sleep(5)
    # 查找需连接的WiFi，并以此作为是否继续执行的依据
        count = 0
        while count <= 5:
            if d(resourceId="android:id/title", text=ssid).exists():
                d(resourceId="android:id/title", text=ssid).click()
                time.sleep(5)
                d(resourceId="com.android.settings:id/password").click()
                d.send_keys(password, clear=True)
                time.sleep(2)
                d(resourceId="android:id/button1").click()
                time.sleep(10)
                a = get_wlan0_android14(udid)
                if a.count(".") == 3:
                    print(str(udid) + ' ip: ' + a + '\n')
                    result = "True"
                elif a.count(":") >= 2:
                    print(str(udid) + ' ipv6: ' + a + '\n')
                    result = "True"
                else:
                    result = "获取IP地址失败：False"
                break
            else:
                print("手机{udid}未搜到{ssid}的WiFi，下滑页面继续查找")
                d.swipe(394, 1600, 394, 600, steps=20)
                count += 1

    except Exception as e:
        print("手机设连接wifi失败 :{e}")
        result = 'False'
    finally:
        d.app_stop("com.android.settings")
        return result
def click_close_wifi(udid, ssid):
    """
       功能：
           1.手机通过点击WLAN，找到指定的已保存的网络删除
           2.点击SSID后，删除网络
           3.该接口，受手机型号限制，
           4.已经兼容了HONOR
       参数：
           udid：手机的udid
           ssid：手机所连接的无线服务
       返回值：
           点击成功返回'True',失败返回'False'
       举例：
   click_close_wifi('2eb38cdb','ssid_1',)
       作者/日期：
       duanwnexing/2023/10/17    zhengchao--20240528 修改兼容红米K70P
   """
    result = 'False'
    mobile_phone_brand = get_mobile_phone_brand_android14(udid)
    activity = ".Settings"
    if mobile_phone_brand == "HONOR":
        activity = ".HWSettings"
        os.system("adb -s " + str(udid) + " shell input keyevent 3")
    try:
        d = u2.connect(str(udid))
        time.sleep(1)
        d.uiautomator.start()
        time.sleep(1)
        # 切换成 ui2 的输入法，这里会隐藏掉系统原本的输入法 , 默认是使用系统输入法
        # 当传入 False 时会使用系统默认输入法，默认为 Fasle
        d.set_fastinput_ime(True)
        # 查看当前输入法
        print(d.current_ime())
        print("False 时会使用系统默认输入法'")
    # 打开设置
        try:
            d.app_start("com.android.settings", activity, stop=True)
        except:
            d.app_start("com.android.settings", stop=True)
        time.sleep(3)
    # 点击WLAN
        d(resourceId="android:id/title", text="WLAN").click()
        time.sleep(5)
    # 查找需连接的WiFi，并以此作为是否继续执行的依据
        count = 0
        while count <= 5:
            if d(resourceId="android:id/title", text=ssid).exists():
#                 d(resourceId="android:id/title", text=ssid).click()
#                 time.sleep(3)
#                 #点击完成
#                 d(resourceId="android:id/button1").click()
                time.sleep(3)
                ssidDescrip = ssid + ' 网络详情'
                print('ssidDescrip:',ssidDescrip)
                d(resourceId="com.android.settings:id/preference_detail", description=ssidDescrip).click()
#                d.xpath('//*[@resource-id="com.android.settings:id/scroll_headers"]/android.widget.LinearLayout[4]/android.widget.RelativeLayout[1]').click()
#                d(className="android.widget.ImageView", resourceId="com.android.settings:id/preference_detail").click()
                time.sleep(3)
                #下滑页面
                d.swipe(394, 1600, 394, 600, steps=20)
                d(resourceId="android:id/title", text="删除网络").click()
                d(resourceId="android:id/button1").click()
                result = "True"
                break
            else:
                print("手机{udid}未搜到{ssid}的WiFi，下滑页面继续查找")
                d.swipe(394, 1600, 394, 600, steps=20)
                count += 1

    except Exception as e:
        print("删除已管理手机失败，请检查相关日志信息:{e}")
        result = 'False'
    finally:
        d.app_stop("com.android.settings")
        return result   


def connect_to_wifi(serial_id, ssid, password):
    """
    连接到指定的 WPA2/WPA/WEP Wi-Fi 网络
    :param serial_id: 设备序列号
    :param ssid: Wi-Fi 名称
    :param password: Wi-Fi 密码
    :return: 成功返回 "True"，失败返回错误信息
    """
    try:
        # 启动 Wi-Fi
        os.system(f'adb -s {serial_id} shell svc wifi enable')
        time.sleep(2)

        # 停止已运行的 adb-join-wifi 应用
        os.system(f'adb -s {serial_id} shell am force-stop com.steinwurf.adbjoinwifi')
        time.sleep(1)

        # 构造命令
        base_cmd = f'adb -s {serial_id} shell am start -n com.steinwurf.adbjoinwifi/.MainActivity --esn connect -e ssid "{ssid}"'
        password_cmd = f'-e password_type WPA -e password "{password}"'

        full_cmd = f'{base_cmd} {password_cmd}'
        print("执行命令:", full_cmd)
        os.system(full_cmd)
        time.sleep(5)

        # 检查是否成功获取 IP 地址
        for i in range(5):
            ip = get_wlan0(serial_id)
            if ip and ip.count(".") == 3:
                print(f"该设备{serial_id} 获取到 IP: {ip}")
                return "True"
            time.sleep(5)

        print(f"该设备{serial_id} 未成功连接")
        return "False"

    except Exception as e:
        print(f"连接失败: {e}")
        return f"False: {str(e)}"




import subprocess
import time

def connect_wifi_android10_pass(device_id, ssid, mode, password):
    """
    通过ADB命令连接Android 10及以上版本的WiFi网络

    参数:
        device_id (str): 设备序列号
        ssid (str): WiFi网络名称
        mode (str): 认证模式 (open, wep, wpa2)
        password (str): WiFi密码

        open - 开放网络（无密码）
        wep - WEP 加密网络
        wpa2 - WPA2 加密网络（最常用）
        wpa - WPA 加密网络
        owe - 增强开放网络（ Opportunistic Wireless Encryption ）
        sae - 同步认证（WPA3个人版）
        eap - EAP 认证（企业网络）

    返回:
        bool: 连接成功返回True，失败返回False
    """
    try:
        # # 禁用WiFi
        # subprocess.run(f"adb -s {device_id} shell svc wifi disable",
        #               shell=True, check=True, capture_output=True)
        # time.sleep(1)
        #
        # # 启用WiFi
        # subprocess.run(f"adb -s {device_id} shell svc wifi enable",
        #               shell=True, check=True, capture_output=True)
        # time.sleep(2)

        # 构造并执行连接命令
        cmd = f'adb -s {device_id} shell cmd wifi connect-network "{ssid}" {mode} "{password}"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        # 检查执行结果
        if result.returncode != 0:
            error_msg = result.stderr.strip() if result.stderr else "连接WiFi失败"
            print(f"连接WiFi失败: {error_msg}")
            return False

        print(f"成功连接到WiFi: {ssid}")

        # 获取IP地址
        # 等待并检查是否成功获取IP地址
        for i in range(5):
            ip = get_wlan0(device_id)
            if ip and ip.count(".") == 3:
                print(f"设备 {device_id} 获取到IP地址: {ip}")
                return True
            time.sleep(5)

        print(f"设备 {device_id} 未能成功获取IP地址")
        return False

    except subprocess.CalledProcessError as e:
        print(f"执行ADB命令时出错: {e.stderr.decode() if e.stderr else str(e)}")
        return False
    except Exception as e:
        print(f"连接WiFi时发生异常: {str(e)}")
        return False




if __name__ == '__main__':
  
    # udid = "Z5Y5KZY9LZRS69JF"
    # adb_close_wifi('Z5Y5KZY9LZRS69JF',"00*h2e-V9")
    # time.sleep(5)

    
    pass


