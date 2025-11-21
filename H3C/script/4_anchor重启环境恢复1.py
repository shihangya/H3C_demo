from function import *


def anchor_restart():
    AC = connect("qx1240")
    AC.send(f'''
     wlan ap ap1
     
     radio 1
   undo service-template m1
  undo service-template m2
  undo service-template m3
  undo service-template m4
  radio 2
    undo service-template m1
  undo service-template m2
  undo service-template m3
  undo service-template m4
  radio 3
    undo service-template m1
  undo service-template m2
  undo service-template m3
  undo service-template m4
     
     wlan ser m3
     undo ser en
     y
     undo mlo en
     ser en
     
     wlan ser m4
     undo ser en
      y
      undo mlo en
      ser en
     
     
     wlan ap ap1
  dis th
     
     
     radio 1
       service-template m1
  service-template m2
  service-template m3
  service-template m4
  radio 2
    service-template m1
  service-template m2
  service-template m3
  service-template m4
  radio 3
    service-template m1
  service-template m2
  service-template m3
  service-template m4
  wlan ap ap1
  dis th
  
  
  wlan ser m1
  undo ser en
  y
  
  undo mlo en
  
  
  
       wlan ser m3
     undo ser en
     y
     mlo en
     ser en
     

  
  wlan ap ap1
  dis th
  
  wlan ser m2
  undo ser en
   y
   undo mlo en
   
        wlan ser m4
     undo ser en
      y
       mlo en
      ser en
   
   wlan ap ap1
  dis th
 wlan ap ap1
 
   radio 2
   radio dis 
   
   
   wlan ap ap1
  dis th
  radio 2
   radio en
   
   wlan ap ap1
  dis th

   wlan ser m1
   
   ser en
   wlan ap ap1
  dis th
   wlan ser m2
   
   ser en
   wlan ap ap1
  dis th

   wlan ap ap1
   dis th
   
  
    
                    '''
            )

def fitAc_restart():
    AC1 = connect("2520x")
    AC1.send(f'''
     wlan ap ap6
    
     
     radio 1
   undo service-template m1
  undo service-template m2
  undo service-template m3
  undo service-template m4
  radio 2
    undo service-template m1
  undo service-template m2
  undo service-template m3
  undo service-template m4
  radio 3
    undo service-template m1
  undo service-template m2
  undo service-template m3
  undo service-template m4
     
     
     
     
     radio 1
       service-template m1
  service-template m2
  service-template m3
  service-template m4
  radio 2
    service-template m1
  service-template m2
  service-template m3
  service-template m4
  radio 3
    service-template m1
  service-template m2
  service-template m3
  service-template m4
  
  wlan ser m1
  undo ser en
  y
  undo mlo en
  wlan ser m2
  undo ser en
   y
   undo mlo en
   dis wlan bss all
   dis wlan bss all v | in MLO
   wlan ap ap6
   dis th
   radio 2
   radio dis 
   radio en
   radio en
   dis wlan bss all
   dis wlan bss all v | in MLO
   wlan ap ap6
   dis th
   wlan ser m1
   mlo en
   ser en
   wlan ser m2
   mlo en
   ser en
   dis wlan bss all
   dis wlan bss all v | in MLO
   wlan ap ap6
   dis th
                    '''
            )


if __name__ == '__main__':


    anchor_restart()
    # fitAc_restart()
