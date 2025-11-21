import time

from function import *


def AP_down():
    SW  = connect("s5120")
    SW.send(f''' 
        sys
        int g1/0/14
        shutdown
        undo shutdown       
    ''')

def AC_send_bind_service():
    AC = connect("2520x")
    AC.send(f''' 
            wlan ap ap1
            radio 1
            service-template m1
            service-template m2
            service-template m5
            service-template m6
            service-template m11
            service-template m10
            service-template m12
            service-template m3
            service-template m4
            service-template m8
            service-template m7
            service-template m9
            service-template m14
            service-template m13
            service-template m15
            radio 2    
            service-template m15
            service-template m14
            service-template m13
            service-template m12
            service-template m11
            service-template m10
            service-template m9
            service-template m8
            service-template m7
            service-template m6
            service-template m5
            service-template m4
            service-template m3
            service-template m2
            service-template m1
            radio 3
            service-template m1
            service-template m2
            service-template m3
            service-template m4
            service-template m5
            service-template m6
            service-template m7
            service-template m8
            service-template m9
            service-template m10
            service-template m11
            service-template m12
            service-template m13
            service-template m14
            service-template m15
  
    
        ''')


def AC_send_unbind_service():
    AC = connect("2520x")
    AC.send(f''' 
            
            wlan ap ap1
            radio 1
            undo service-template m8
            undo service-template m13
            undo service-template m5
            undo service-template m6
            undo service-template m11
            undo service-template m10
            undo service-template m12
            undo service-template m3
            undo service-template m4
            undo service-template m1
            undo service-template m7
            undo service-template m9
            undo service-template m14
            undo service-template m2
            undo service-template m15
            radio 2    
            undo service-template m15
            undo service-template m14
            undo service-template m13
            undo service-template m12
            undo service-template m11
            undo service-template m10
            undo service-template m9
            undo service-template m8
            undo service-template m7
            undo service-template m6
            undo service-template m5
            undo service-template m4
            undo service-template m3
            undo service-template m2
            undo service-template m1
            radio 3
            undo service-template m1
            undo service-template m2
            undo service-template m3
            undo service-template m4
            undo service-template m5
            undo service-template m6
            undo service-template m7
            undo service-template m8
            undo service-template m9
            undo service-template m10
            undo service-template m11
            undo service-template m12
            undo service-template m13
            undo service-template m14
            undo service-template m15


        ''')


if __name__ == '__main__':
    while True:

        # AC_send_bind_service()
        # AP_down()
        # time.sleep(2)
        AC_send_unbind_service()
        time.sleep(200)