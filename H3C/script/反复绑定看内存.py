from function import *

# t = ("g0","g1","g2","g3","g4","g5","g6","g7","g8","g9","g10","g11","g12","g13","g14","g15")
# t1 = ("g0","g1","g2","g3","g4","g5","g6","g7","g8","g9","g10","g11","g12","g13","g14","g15")
# i = 0
# while 1 > 0 :
#     for i in range(0,16):
#         dut.send(f"""
#                     interface WLAN-Radio 1/0/1
#                     wlan service-template {t[i]}
#                     interface WLAN-Radio 1/0/2
#                     wlan service-template {t[i]}
#                     interface WLAN-Radio 1/0/3
#                     wlan service-template {t[i]}
#                 """)
#     print(t[i])
#     i += 1
#     if i == len(t):   # 判断是否到元组末尾
#         i = 0


#     time.sleep(0.5)


# 定义服务模板和接口
templates = ("g0", "g1", "g2", "g3", "g4", "g5", "g6", "g7",
             "g8", "g9", "g10", "g11", "g12", "g13", "g14", "g15")
interfaces = ["WLAN-Radio 1/0/1", "WLAN-Radio 1/0/2", "WLAN-Radio 1/0/3"]

# 控制是 apply 还是 undo
mode = 0  # 0: apply, 1: undo

while True:

    for template in templates:
        print(f"Mode: {'apply' if mode % 2 == 0 else 'undo'}, Template: {template}")
        for intf in interfaces:
            if mode % 2 == 0:
                dut.send(f"""
                            interface {intf}
                            service-template {template}
                            """
                         )
            else:
                dut.send(f"""
                            interface {intf}
                            undo service-template {template}
                        """)
            # time.sleep(1)  # 每个接口之间等待5秒

    mode += 1  # 切换模式
    time.sleep(3)  # 每轮结束后等待10秒

    dut.send(f"""
            di {mode} ci
            dis memory
         """
             )

