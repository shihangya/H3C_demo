from function import *


def anchor_restart():
    AC = connect("qx1240")
    AC.send(f'''
     wlan ap ap1
     radio 2
     radio disable
     radio 1
    
      undo service-template g1
      undo service-template g2
      undo service-template g3
      undo service-template g4
      undo service-template g5
      undo service-template g6
      undo service-template g7
      undo service-template g8
      undo service-template g9
      undo service-template g10
      undo service-template g11
      undo service-template g12
      undo service-template g13
      undo service-template g14
      undo service-template g15
      undo service-template m1
      undo service-template m2
    
    
      radio 2
      undo service-template g1
      undo service-template g2
      undo service-template g3
      undo service-template g4
      undo service-template g5
      undo service-template g6
      undo service-template g7
      undo service-template g8
      undo service-template g9
      undo service-template g10
      undo service-template g11
      undo service-template g12
      undo service-template g13
      undo service-template g14
      undo service-template g15
      undo service-template m1
      undo service-template m2
    
    
      radio 3
      undo service-template g1
      undo service-template g2
      undo service-template g3
      undo service-template g4
      undo service-template g5
      undo service-template g6
      undo service-template g7
      undo service-template g8
      undo service-template g9
      undo service-template g10
      undo service-template g11
      undo service-template g12
      undo service-template g13
      undo service-template g14
      undo service-template g15
      undo service-template m1
      undo service-template m2
    
      radio 1
    
      service-template m1
      service-template m2
      service-template g3
      service-template g4
      service-template g5
      service-template g6
      service-template g7
      service-template g8
      service-template g9
      service-template g10
      service-template g11
      service-template g12
      service-template g13
      service-template g14
      
    
    
      radio 2
      service-template g1
      service-template m1
      service-template m2
      service-template g4
      service-template g5
      service-template g6
      service-template g7
      service-template g8
      service-template g9
      service-template g10
      service-template g11
      service-template g12
      service-template g13
      service-template g14
      
    
      radio 3
      service-template g1
      service-template g2
      service-template m1
      service-template m2
      service-template g5
      service-template g6
      service-template g7
      service-template g8
      service-template g9
      service-template g10
      service-template g11
      service-template g12
      service-template g13
      service-template g14
      
    
      radio 2 
      radio enable
    
                    '''
            )

def fitAc_restart():
    AC1 = connect("2520x")
    AC1.send(f'''
     wlan ap ap6
     radio 2
     radio disable
     radio 1
    
      undo service-template g1
      undo service-template g2
      undo service-template g3
      undo service-template g4
      undo service-template g5
      undo service-template g6
      undo service-template g7
      undo service-template g8
      undo service-template g9
      undo service-template g10
      undo service-template g11
      undo service-template g12
      undo service-template g13
      undo service-template g14
      undo service-template g15
      undo service-template m1
      undo service-template m2
    
    
      radio 2
      undo service-template g1
      undo service-template g2
      undo service-template g3
      undo service-template g4
      undo service-template g5
      undo service-template g6
      undo service-template g7
      undo service-template g8
      undo service-template g9
      undo service-template g10
      undo service-template g11
      undo service-template g12
      undo service-template g13
      undo service-template g14
      undo service-template g15
      undo service-template m1
      undo service-template m2
    
    
      radio 3
      undo service-template g1
      undo service-template g2
      undo service-template g3
      undo service-template g4
      undo service-template g5
      undo service-template g6
      undo service-template g7
      undo service-template g8
      undo service-template g9
      undo service-template g10
      undo service-template g11
      undo service-template g12
      undo service-template g13
      undo service-template g14
      undo service-template g15
      undo service-template m1
      undo service-template m2
    
      radio 1
    
      service-template m1
      service-template m2
      service-template g3
      service-template g4
      service-template g5
      service-template g6
      service-template g7
      service-template g8
      service-template g9
      service-template g10
      service-template g11
      service-template g12
      service-template g13
      service-template g14
      service-template g15
    
    
      radio 2
      service-template g1
      service-template m1
      service-template m2
      service-template g4
      service-template g5
      service-template g6
      service-template g7
      service-template g8
      service-template g9
      service-template g10
      service-template g11
      service-template g12
      service-template g13
      service-template g14
      service-template g15
    
      radio 3
      service-template g1
      service-template g2
      service-template m1
      service-template m2
      service-template g5
      service-template g6
      service-template g7
      service-template g8
      service-template g9
      service-template g10
      service-template g11
      service-template g12
      service-template g13
      service-template g14
      service-template g15
      
    
      radio 2 
      radio enable
    
                    '''
            )


if __name__ == '__main__':
    while True:

        anchor_restart()
        fitAc_restart()
