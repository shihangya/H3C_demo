from function.android import *
from function.miji import *



# while True:
#
#     connect_to_wifi("ZY22GCD32Q","mlo*6+5","123123123")
#     a = get_wlan0_android14('ZY22GCD32Q')
#     print("STA IP 为：" + a)
#     multi_ping(['ZY22GCD32Q'],'8.1.1.231')
AC = connect("2520x")
while True:
    # connect_to_wifi("Z5Y5KZY9LZRS69JF","guajiceshi","123123123")
    AC.send(f'''
                sys
                wlan ser 20
                undo ser enable
                Y
                ssid 00h00h00h
                ser en
                quit
                quit
                dis wlan client
                reset wlan client all
                Y
                reset wlan client all
                Y
                dis wlan client
                ''')
    connect_to_wifi("Z5Y5KZY9LZRS69JF", "00h00h00h", "123123123")
    # multi_all("00h00h00h")
    AC.send('''
                sys
                wlan ser 20
                undo ser enable
                Y
                ssid 00h00h00h-00
                ser en
                quit
                quit
                dis wlan client
                reset wlan client all
                Y
                reset wlan client all
                Y
                dis wlan client
                ''')
    # multi_all("00h00h00h-00")
    connect_to_wifi("Z5Y5KZY9LZRS69JF", "00h00h00h-00", "123123123")
    time.sleep(3)

# multi_all("2580x-owe")

