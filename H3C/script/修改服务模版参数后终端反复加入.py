import time

from function.android import *
from function.miji import *
import threading



# while True:
#
#     connect_to_wifi("ZY22GCD32Q","mlo*6+5","123123123")
#     a = get_wlan0_android14('ZY22GCD32Q')
#     print("STA IP 为：" + a)
#     multi_ping(['ZY22GCD32Q'],'8.1.1.231')


AC = connect("2520x")
# AP = connect("qianlan")
while True:
    # connect_to_wifi("Z5Y5KZY9LZRS69JF","guajiceshi","123123123")
    # AP.send("""
    #             dis wlan bss all
    #     """)
    AC.send(f'''
                dis wlan bss all ver | in MLO
                sys
                dis wlan client 
                dis wlan client verbose  | inc MLO
                wlan ser wpa3-h2e
                undo ser enable
                Y
                client-security ignore-authentication
                client forwarding-location ac
                
                ''')
    output = AC.send('''mlo enable ''')
    print(f"输出为：{output}")
    if "f" in output:
        break

    AC.send(f'''
                    
                   
                    ssid 0303035999
                    ser en
                    quit
                    quit
                    dis wlan client
                    dis wlan client verbose  | inc MLO
                    reset wlan client all
                    Y
                    reset wlan client all
                    Y
                    dis wlan client
                    dis wlan client verbose  | inc MLO
                    dis wlan bss all ver | in MLO 
                    ''')
    time.sleep(5)
    connect_to_wifi("Z5Y5KZY9LZRS69JF", "0303035999", "123123123")
    # connect_to_wifi("ZY22GCD32Q", "0303035999", "123123123")
    # 使用多线程同时连接WiFi
    # thread1 = threading.Thread(target=connect_to_wifi, args=("Z5Y5KZY9LZRS69JF", "0303035999", "123123123"))
    # thread2 = threading.Thread(target=connect_to_wifi, args=("ZY22GCD32Q", "0303035999", "123123123"))

    # thread1.start()
    # thread2.start()

    # thread1.join()
    # thread2.join()





    AC.send('''
                dis wlan bss all ver | in MLO
                sys
                dis wlan client
                dis wlan client verbose  | inc MLO
                wlan ser wpa3-h2e
                undo ser enable
                Y
                client forwarding-location ap
                undo client-security ignore-authentication
                vlan 1
                
                ''')

    output = AC.send('''undo mlo enable ''')
    print(f"输出为：{output}")
    if "f" in output:
        break

    AC.send('''

                ssid 0202035888
                ser en
                quit
                quit
                dis wlan client
                dis wlan client verbose  | inc MLO
                reset wlan client all
                Y
                reset wlan client all
                Y
                dis wlan client
                dis wlan client verbose  | inc MLO
                dis wlan bss all ver | in MLO
                ''')
    time.sleep(5)
    connect_to_wifi("Z5Y5KZY9LZRS69JF", "0202035888", "123123123")
    # connect_to_wifi("ZY22GCD32Q", "0303035999", "123123123")
    # 使用多线程同时连接WiFi
    # thread1 = threading.Thread(target=connect_to_wifi, args=("Z5Y5KZY9LZRS69JF", "0303035999", "123123123"))
    # thread2 = threading.Thread(target=connect_to_wifi, args=("ZY22GCD32Q", "0303035999", "123123123"))

    # thread1.start()
    # thread2.start()

    # thread1.join()
    # thread2.join()




