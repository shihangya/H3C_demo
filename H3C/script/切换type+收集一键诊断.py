from function.miji import *
import time

AC = connect("2520x")
AP = connect("qianlan")
i = 1
while True:
    if i == 1:
        try:
            AC.send('''
                    dis wlan bss all verbose | in MLO
                    wlan ap ap1
                    ''')
            time.sleep(1)
            AC.send('''
                    radio 1
                    ''')
            time.sleep(1)
            AC.send('''
                    type dot11be
                    Y
                    Y
                    ''')
            time.sleep(10)
            AC.send('''
                        dis wlan bss all verbose | in MLO
                        wlan ap ap1
                        ''')
            time.sleep(1)
            AC.send('''
                        radio 1
                        ''')
            time.sleep(1)
            AC.send('''
                        type dot11abe
                        Y
                        Y
                        ''')
            time.sleep(10)

            result = AC.CheckCommand('AP是否在线',
                                     cmd='ping 77.88.3.17',
                                     expect=['5 packet(s) transmitted, 5 packet(s) received, 0.0% packet loss'],
                                     expect_count=1,
                                     stop_max_attempt=3,
                                     relationship='and',
                                     wait_fixed=3
                                     )
            if result:
                print("AP在线")
            else:
                time.sleep(180)
                AP.send('''
                    a
                    a
                    a
                    a
                    a
                    a
                    a
                    sys
                    probe
                    dis diagnostic-information
                    Y
                    diag_ap1_ap.tar.gz
                    Y
                    ''')
                print("Ping检查失败")
                i += 1

        except Exception as e:
            print(f"执行过程中发生异常: {e}")
    else:
        break