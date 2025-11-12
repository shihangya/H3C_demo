from function.miji import *

AC = connect("2520x")
MackLog()

while True:
    now = datetime.now()

    AC.send('''
            radio 1
             service-template g1
              service-template g2
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
              service-template g0
            ''')
    hsh = AC.send('''
            radio 2
             service-template m2
            ''')
    right = "The service has exceeded the specification, cannot bind the mlo service template."
    if hsh == right:
        print("检查成功")
    else:
        print("================================检查失败=======================================================================")
        print(now.time())

    AC.send('''
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
    undo service-template g0
            ''')
    AC.send('''
            radio 2
             undo service-template m2
            ''')
