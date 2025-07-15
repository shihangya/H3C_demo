from mokuai.miji import *

ac1 = connect("3520X-G")
ac2 = connect("3520X-GBei")
for i in range(520):
    
    
    ac1.send(f"""
                
                display wlan client verbose | inc MAC address
                
                display wlan client verbose | inc MLO status

                display wlan client verbose | inc Online time

                dis wlan client
            """)
    ac2.send(f"""
                
                display wlan client verbose | inc MAC address
                
                display wlan client verbose | inc MLO status

                display wlan client verbose | inc Online time

                dis wlan client
            """)
    
    
    
    time.sleep(2)