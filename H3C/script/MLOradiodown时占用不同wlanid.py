from function.service import *
AC = connect("wwx5580H")

AC.send(f'''
                       radio 1
                       ser wpa3-h2e
                       ser wpa3-hnp
                       ser g1
                       ser g2
                       ser g3
                       ser g4
                       ser g5
                       ser g6
                       ser g7
                       ser g8
                       ser g9
                       ser g10
                        ser g11
                        ser g12
                        ser g13
                       radio 2
                       ser g1
                       ser g2
                       ser wpa3-h2e
                       ser wpa3-hnp
                       ser g3
                       ser g4
                       ser g5
                       ser g6
                       ser g7
                       ser g8
                       ser g9
                       ser g10
                        ser g11
                        ser g12
                        ser g13
                       radio 3
                       ser g1
                       ser g2
                       ser g3
                       ser g4
                       ser wpa3-h2e
                       ser wpa3-hnp                       
                       ser g5
                       ser g6
                       ser g7
                       ser g8
                       ser g9
                       ser g10
                        ser g11
                        ser g12
                        ser g13
                                             
                       '''
            )