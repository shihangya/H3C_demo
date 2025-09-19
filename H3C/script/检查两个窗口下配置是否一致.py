import time
from function.service import *
import random

AC = connect("wx3510x")
AC1 = connect("wx3510x_1")
yizhi = 1
buyizhi = 1

moban1 = ("g0", "g1", "g2", "g3", "g4", "g5", "g6", "g7", "g8", "g9", "g10", "g11", "g12", "g13", "g14")
moban2 = ("wpa3-h2e", "wpa3-hnp","wpa3-both")
while True:
    # 从moban1中随机取13个元素
    random_moban1 = random.sample(moban1, 13)

    # 从moban2中随机取2个元素（因为min(2, len(moban2)) = 2）
    random_moban2 = random.sample(moban2, 2)

    # 生成moban3，将两个随机选取的列表合并
    moban3 = random_moban1 + random_moban2
    print(f"moban3长度: {len(moban3)}，内容: {moban3}")

    # 生成六个随机顺序的moban3变体
    moban3_1 = random.sample(moban3, len(moban3))
    moban3_2 = random.sample(moban3, len(moban3))
    moban3_3 = random.sample(moban3, len(moban3))
    moban3_4 = random.sample(moban3, len(moban3))
    moban3_5 = random.sample(moban3, len(moban3))
    moban3_6 = random.sample(moban3, len(moban3))

    # 循环次数应与moban3的长度一致，即15次
    for i in range(len(moban3)):  # 使用len(moban3)确保不会越界
        AC.send(f"""
            wlan ap ap1
            radio 1
            ser {moban3_1[i]}
            radio 2
            ser {moban3_2[i]}
            radio 3
            ser {moban3_3[i]}
            """
        )
        AC1.send(f"""
                wlan ap ap1
                radio 1
                ser {moban3_4[i]}
                radio 2
                ser {moban3_5[i]}
                radio 3
                ser {moban3_6[i]}
                """
                 )



    time.sleep(5)
        # 检查
    a=AC.send("""
    dis wlan bss all
    """)
    b=AC1.send("""
    dis wlan bss all
    """)
    time.sleep(3)
    if a == b:

        yizhi = yizhi + 1
        print("配置一致:" + str(yizhi))
    else:
        buyizhi = buyizhi + 1
        print("配置不一致:" + str(buyizhi))

        # 清理配置 - 两个设备都应该执行undo命令
    for i in range(len(moban3)):
        AC.send(f"""
            wlan ap ap1
            radio 1
            undo ser {moban3_1[i]}
            radio 2
            undo ser {moban3_2[i]}
            radio 3
            undo ser {moban3_3[i]}
            """
        )
        AC1.send(f"""
                wlan ap ap1
                radio 1
                undo ser {moban3_4[i]}
                radio 2
                undo ser {moban3_5[i]}
                radio 3
                undo ser {moban3_6[i]}
                """
                 )


