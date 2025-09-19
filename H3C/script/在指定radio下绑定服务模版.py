from function.service import *

AC = connect("wx3510x")

# moban1 = ("hsh", "hsh1", "wpa2-persion", "wpa3-qiye", "66", "mac")
moban1 = ("g0", "g1", "g2", "g3", "g4", "g5", "g6", "g7", "g8", "g9", "g10", "g11", "g12", "g13", "g14")
moban2 = ("g14", "g13", "g12", "g11", "g10", "g9", "g8", "g7", "g6", "g5", "g4", "g3", "g2", "g1", "g0")
moban3 = ("g7", "g8", "g9", "g10", "g11", "g0", "g1", "g2", "g3", "g4", "g5", "g6", "g12", "g13", "g14")
a = 1  # 1:绑定  2:取消绑定
radio = 1  # 选择使用那个 radio
i = 1  # 选择使用那个模版

if i == 1:
    moban = moban1
elif i == 2:
    moban = moban2
elif i == 3:
    moban = moban3

if a == 1:

    AC.send(f'''
                       radio {radio}                      
                       '''
            )
    for i in range(0, len(moban)):
        AC.send(f''' 
                    service-template {moban[i]}
                    '''
                )
else:
    AC.send(f'''
                           radio {radio}                      
                           '''
            )
    for i in range(0, len(moban)):
        AC.send(f'''
                        radio {radio}
                        undo service-template {moban[i]}
                        '''
                )
