
from function.miji import *
from function.service import *

MackLog()

AC = connect("2520x1")
while True:
    now = datetime.now()
    print(f"1、AP入组C,{now.strftime('%Y-%m-%d %H:%M:%S')}")
    AC.send(f'''
                sys
                wlan ap-group c
                ap ap00 
                                          
              '''
            )
    print(f"2、重新使能服务模版,{now.strftime('%Y-%m-%d %H:%M:%S')}")
    AC.send(f'''
                sys
                wlan ser wpa3-h2e
                undo ser en
                y
                ser en 
                quit                          
              '''
            )
    print(f"3、终端加入,{now.strftime('%Y-%m-%d %H:%M:%S')}")
    connect_to_wifi("Z5Y5KZY9LZRS69JF", "0202035888", "123123123")
    connect_to_wifi("10ACBN2A22000UH", "0202035888", "123123")
    print(f"4、检查终端是否加入MLO,{now.strftime('%Y-%m-%d %H:%M:%S')}")
    AC.send(f'''
                quit
                dis wlan client ver | in MLO
                                        
              '''
            )
    print(f"5、去使能MLO,{now.strftime('%Y-%m-%d %H:%M:%S')}")
    AC.send(f'''
                sys
                wlan ser wpa3-h2e
                undo ser en
                y
                undo mlo enable
                ser en                           
              '''
            )
    print(f"6、AP入组D,{now.strftime('%Y-%m-%d %H:%M:%S')}")
    AC.send(f'''
                wlan ap-group d
                ap ap00                             
              '''
            )
    print(f"7、重新使能服务模版,{now.strftime('%Y-%m-%d %H:%M:%S')}")
    AC.send(f'''
                wlan ser wpa3-h2e
                undo ser en
                y
                ser en 
                quit                          
              '''
            )
    print(f"8、终端加入,{now.strftime('%Y-%m-%d %H:%M:%S')}")
    connect_to_wifi("Z5Y5KZY9LZRS69JF", "0202035888", "123123123")
    connect_to_wifi("10ACBN2A22000UH", "0202035888", "123123")
    print(f"9、检查终端是否加入MLO,{now.strftime('%Y-%m-%d %H:%M:%S')}")
    AC.send(f'''
                quit
                
                dis wlan client ver | in MLO                          
              '''
            )
    print(f"10、使能MLO,{now.strftime('%Y-%m-%d %H:%M:%S')}")
    AC.send(f'''
                sys
                wlan ser wpa3-h2e
                undo ser en
                y
                mlo enable 
                ser enable                           
              '''
            )
    print(f"11、组C去绑定MLO服务，为了让MLO占最后一位,{now.strftime('%Y-%m-%d %H:%M:%S')}")
    AC.send(f'''
                wlan ap ap00
                radio 1
                undo ser wpa3-h2e
                radio 2
                undo ser wpa3-h2e
                radio 3
                undo ser wpa3-h2e                           
              '''
            )
    print(f"12、AP入组C,{now.strftime('%Y-%m-%d %H:%M:%S')}")
    AC.send(f'''
                wlan ap-group c
                ap ap00                             
              '''
            )
    print(f"13、服务模版绑定至AP视图，占最后一位,{now.strftime('%Y-%m-%d %H:%M:%S')}")
    AC.send(f'''
                wlan ap ap00
                radio 1
                ser wpa3-h2e
                radio 2
                ser wpa3-h2e
                radio 3
                ser wpa3-h2e                           
              '''
            )
    print(f"14、终端加入,{now.strftime('%Y-%m-%d %H:%M:%S')}")
    connect_to_wifi("Z5Y5KZY9LZRS69JF", "0202035888", "123123123")
    connect_to_wifi("10ACBN2A22000UH", "0202035888", "123123")
    print(f"15、检查终端是否加入MLO,{now.strftime('%Y-%m-%d %H:%M:%S')}")
    AC.send(f'''
                quit
                
                dis wlan client ver | in MLO                          
              '''
            )
    print(f"16、AP视图去绑定MLO服务，加入一个普通服务，占f位，占完后删除该普通服务,{now.strftime('%Y-%m-%d %H:%M:%S')}")
    AC.send(f'''
                sys
                
                wlan ap ap00
                radio 1
                undo ser wpa3-h2e
                y
                radio 2
                undo ser wpa3-h2e
                y
                radio 3
                undo ser wpa3-h2e 
                y
                radio 1
                ser g0
                ser wpa3-h2e 
                radio 2
                ser wpa3-h2e   
                radio 3
                ser wpa3-h2e  
                radio 1
                undo ser g0                                           
              '''
            )
    print(f"17、终端加入,{now.strftime('%Y-%m-%d %H:%M:%S')}")
    connect_to_wifi("Z5Y5KZY9LZRS69JF", "0202035888", "123123123")
    connect_to_wifi("10ACBN2A22000UH", "0202035888", "123123")
    print(f"18、检查终端是否加入MLO,{now.strftime('%Y-%m-%d %H:%M:%S')}")
    AC.send(f'''
                quit
                
                dis wlan client ver | in MLO                          
              '''
            )
    CheckApOnline("2520x1","77.88.0.7")





