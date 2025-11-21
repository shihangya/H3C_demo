from function import *

AC = connect("2520x2")
apid = 11
apname = "ap6"
while True:
    AC.send(f'''
                    
                    sys
                    probe
                    dis system internal wlan private-info ap {apid} MLO
                    dis system internal wlan private-info ap  {apid} | in MLO
                    
                    dis wlan bss ap {apname}
                    dis wlan bss ap {apname} v | in MLO
                    
                    
                    dis system internal wlan private-info ap {apid} MLO
                    dis system internal wlan private-info ap  {apid} | in MLO
                    dis wlan bss ap {apname} v | in MLO
                        
                        
                    dis system internal wlan private-info ap {apid} mlo
                    dis system internal wlan private-info ap  {apid} | in MLO
                    
                    dis sys int wlan ap name {apname} radio 1 | in Wlan
                    dis sys int wlan ap name {apname} radio 2 | in Wlan
                    dis sys int wlan ap name {apname} radio 3 | in Wlan
                                  
                '''
            )
    time.sleep(3)




