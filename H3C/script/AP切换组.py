from function import *


AC = connect("3520h_1")

while True:

    AC.send('''
            display wlan client verbose | inc "MAC address"
                
                display wlan client verbose | inc "MLO status"

                display wlan client verbose | inc "Online time"

                dis wlan client
            sys
            wlan ap-group test_1
            ap ap1  
            quit
            dis wlan ap all   
            ''')
    time.sleep(2)
    connect_to_wifi("Z5Y5KZY9LZRS69JF", "wpa3-h2e-7538", "123123123")
    AC.send('''
            display wlan client verbose | inc "MAC address"
                
                display wlan client verbose | inc "MLO status"

                display wlan client verbose | inc "Online time"

                dis wlan client
            sys
            wlan ap-group test_2
            ap ap1    
            quit
            dis wlan ap all  
            ''')
    connect_to_wifi("Z5Y5KZY9LZRS69JF", "wpa3-h2e-7539", "123123123")
