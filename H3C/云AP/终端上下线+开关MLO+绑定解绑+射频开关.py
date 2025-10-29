from function.miji import *
from function.service import *

AP = connect("722222")
MackLog()

while True:
    now = datetime.now()

    # connect_to_wifi("Z5Y5KZY9LZRS69JF", "0202035888", "123123123")
    print(f"1、删掉服务模版{now.strftime('%Y-%m-%d %H:%M:%S')}")
    AP.send(f'''
                    sys
                    dis wlan client ver | in MLO
                    interface WLAN-Radio 1/0/1
                    undo ser wpa3-h2e
                    interface WLAN-Radio 1/0/2
                    undo ser wpa3-h2e                             
                  '''
                )
    print(f"2、删掉MLO{now.strftime('%Y-%m-%d %H:%M:%S')}")
    AP.send(f'''
                    wlan ser wpa3-h2e
                    undo ser en
                    y
                    undo mlo en
                    ser en                             
                  '''
                )
    print(f"3、绑定服务模版{now.strftime('%Y-%m-%d %H:%M:%S')}")
    AP.send(f'''
                    sys
                    interface WLAN-Radio 1/0/1
                    ser wpa3-h2e
                    interface WLAN-Radio 1/0/2
                    ser g1
                    ser wpa3-h2e                             
                  '''
                )
    print(f"4、终端加入{now.strftime('%Y-%m-%d %H:%M:%S')}")
    connect_to_wifi("Z5Y5KZY9LZRS69JF", "0202035888", "123123123")
    print(f"5、删掉服务模版{now.strftime('%Y-%m-%d %H:%M:%S')}")
    AP.send(f'''
                    sys
                    dis wlan client ver | in MLO
                    interface WLAN-Radio 1/0/1
                    undo ser wpa3-h2e
                    interface WLAN-Radio 1/0/2
                    undo ser wpa3-h2e                             
                  '''
                )
    print(f"6、开启MLO{now.strftime('%Y-%m-%d %H:%M:%S')}")
    AP.send(f'''
                    wlan ser wpa3-h2e
                    undo ser en
                    y
                    mlo en
                    ser en                             
                  '''
                )
    print(f"7、绑定服务模版{now.strftime('%Y-%m-%d %H:%M:%S')}")
    AP.send(f'''
                    sys
                    interface WLAN-Radio 1/0/1
                    ser wpa3-h2e
                    interface WLAN-Radio 1/0/2
                    ser wpa3-h2e                             
                  '''
                )
    print(f"8、终端加入{now.strftime('%Y-%m-%d %H:%M:%S')}")
    connect_to_wifi("Z5Y5KZY9LZRS69JF", "0202035888", "123123123")
    print(f"9、radio down{now.strftime('%Y-%m-%d %H:%M:%S')}")
    AP.send(f'''
                    sys
                    dis wlan client ver | in MLO
                    interface WLAN-Radio 1/0/1
                    shutdown
                    interface WLAN-Radio 1/0/2
                    shutdown 
                    undo ser g1                           
                  '''
                )
    print(f"10、radio up{now.strftime('%Y-%m-%d %H:%M:%S')}")

    AP.send(f'''
                    sys
                    interface WLAN-Radio 1/0/1
                    undo shutdown
                    interface WLAN-Radio 1/0/2
                    undo shutdown                            
                  '''
                )
    print(f"11、终端加入{now.strftime('%Y-%m-%d %H:%M:%S')}")
    connect_to_wifi("Z5Y5KZY9LZRS69JF", "0202035888", "123123123")




