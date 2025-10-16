from function.service import *

AC = connect("wwx5580H_copy")

# 1:raido 开启   2:radio 关闭
a = 1

if a == 1:

    AC.send(f'''
                 wlan ap-group b
                 radio 2
                 radio enable
                 radio 5
                 radio en
                   quit
                   quit
                   wlan ap ap1                 
                       '''
            )
else:
    AC.send(f'''
                     wlan ap-group b
                     radio 2
                     radio disable
                     radio 5
                     radio disable
                    quit
                    quit
                    wlan ap ap1
                           '''
            )