from function.service import *




AC = connect("3520h_1")

moban1 = ("hsh","hsh1","wpa2-persion","wpa3-qiye","66","mac")
# moban1 = ("g0","g1","g2","g3","g4","g5","g6","g7","g8","g9","g10","g11","g12","g13","g14","g15")
moban2= ("g15","g16","g17","g18","g19","g20","g21","g22","g23","g24","g25","g26","g27","g28","g29")
moban3 = ("g30","g31","g32","g33","g34","g35","g36","g37","g38","g39","g40","g41","g42","g43","g44")
a = 1     # 1:绑定  2:取消绑定
if a == 1:
    for i in range(0, len(moban1)):
        AC.send(f'''
                    radio 1
                    service-template {moban1[i]}
                    radio 2
                    service-template {moban1[i]}
                    radio 3
                    service-template {moban1[i]}
                   
                    '''
                )
else:
    for i in range(0, len(moban1)):
        AC.send(f'''
                        radio 1
                        undo service-template {moban1[i]}
                        
                        radio 2
                        undo service-template {moban1[i]}
                        
                        radio 3
                        undo service-template {moban1[i]}
                        
                        '''
                )