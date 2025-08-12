from function.android import *
from function.miji import *



# while True:
#
#     connect_to_wifi("ZY22GCD32Q","mlo*6+5","123123123")
#     a = get_wlan0_android14('ZY22GCD32Q')
#     print("STA IP 为：" + a)
#     multi_ping(['ZY22GCD32Q'],'8.1.1.231')


AC = connect("3520h_kaoji")
while True:
    # connect_to_wifi("Z5Y5KZY9LZRS69JF","guajiceshi","123123123")
    AC.send(f'''
                sys
                dis wlan client
                dis wlan client verbose  | inc MLO
                wlan ser 20
                undo ser enable
                Y
                ssid 030303
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
                ''')
    # connect_wifi_android10_pass("92232c6b", "030303", "wpa2", "123123123")
    connect_to_wifi("92232c6b", "030303", "123123123")
    # multi_all("00h00h00h")
    AC.send('''
                sys
                dis wlan client
                dis wlan client verbose  | inc MLO
                wlan ser 20
                undo ser enable
                Y
                ssid 020203
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
                ''')
    # multi_all("00h00h00h-00")
    # connect_wifi_android10_pass("92232c6b", "020203", "wpa2", "123123123")
    connect_to_wifi("92232c6b", "020203", "123123123")
    time.sleep(3)

# multi_all("2580x-owe")

