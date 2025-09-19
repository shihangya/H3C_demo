from function import *


AC = connect("wx3510x")




while True:

    AC.send('''
            display wlan client verbose | inc "MAC address"
                
                display wlan client verbose | inc "MLO status"

                display wlan client verbose | inc "Online time"

                dis wlan client
            sys
            wlan ap-group a
            ap ap1  
            quit
            dis wlan ap all   
            ''')
    time.sleep(10)
    result = AC.CheckCommand('AP是否在线',
                             cmd='ping 77.88.1.143',
                             expect=['5 packet(s) transmitted, 5 packet(s) received, 0.0% packet loss'],
                             expect_count=1,
                             stop_max_attempt=3,
                             relationship='and',
                             wait_fixed=3
                             )
    if result:
        print("AP在线")
    else:
        break
    connect_to_wifi("Z5Y5KZY9LZRS69JF", "00#h2e-V9_hsh编码", "123123123")
    AC.send('''
            display wlan client verbose | inc "MAC address"
                
                display wlan client verbose | inc "MLO status"

                display wlan client verbose | inc "Online time"

                dis wlan client
            sys
            wlan ap-group b
            ap ap1    
            quit
            dis wlan ap all  
            ''')
    connect_to_wifi("Z5Y5KZY9LZRS69JF", "00#h2e-V9_hsh编码", "123123123")
    time.sleep(10)
    result = AC.CheckCommand('AP是否在线',
                             cmd='ping 77.88.1.143',
                             expect=['5 packet(s) transmitted, 5 packet(s) received, 0.0% packet loss'],
                             expect_count=1,
                             stop_max_attempt=3,
                             relationship='and',
                             wait_fixed=3
                             )
    if result:
        print("AP在线")
    else:
        break