from function.service import *

AC = connect("2520x1")

# 1:raido 开启   2:radio 关闭
a = 2

if a == 1:

    AC.send(f'''
                 wlan ap-group ap9
                 radio 2
                 radio enable
                 radio 5
                 radio en
                 radio 6
                 radio en
                   quit
                   quit
                   wlan ap ap9  
                   dis wlan ap name ap9 radio               
                       '''
            )
else:
    AC.send(f'''
                     wlan ap-group ap9
                     radio 2
                     radio disable
                     radio 5
                     radio disable
                     radio 6
                     radio disable
                    quit
                    quit
                    wlan ap ap9
                    dis wlan ap name ap9 radio
                           '''
            )