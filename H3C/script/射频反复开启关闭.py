from function.miji import *

AC = connect("2520x")

while True:
    AC.send('''
            sys
            wlan ap ap6
            radio 1
            radio enable
            
            radio 2
            radio enable
            
            ''')
    time.sleep(1)
    AC.send('''
                sys
                wlan ap ap6
                radio 1
                
                radio disable
                radio 2
                radio disable
                
                ''')
    time.sleep(1)

