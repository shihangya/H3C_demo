from function.service import *




AC = connect("2520x1")

moban = ("wpa3-h2e","wpa3-both","g0","g1","g2","g3","g4","g5","g6","g7","g8","g9","g10","g11","g12")
a = 2

if a == 1:
    for i in range(0, len(moban)):
        AC.send(f'''
                    radio 1
                    service-template {moban[i]}
                    radio 2
                    service-template {moban[i]}
                    radio 3
                    service-template {moban[i]}
                    '''
                )
else:
    for i in range(0, len(moban)):
        AC.send(f'''
                        radio 1
                        undo service-template {moban[i]}
                        y
                        y
                        radio 2
                        undo service-template {moban[i]}
                        y
                        y
                        radio 3
                        undo service-template {moban[i]}
                        y
                        y
                        '''
                )