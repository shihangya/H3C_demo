from function.miji import *

AC = connect("qx1240")
# AC1 = connect("2520x3")

# 射频关闭
def radio_diable():
    AC.send(f'''
            
            wlan ap ap1
            radio 1
            radio disable
            
            radio 2
            radio disable
            
            radio 3
            radio disable
            ''')


# 射频开启
def radio_enable():
    AC.send(f'''
            
            wlan ap ap1
            radio 1
            radio enable
            
            radio 2
            radio enable
            
            radio 3
            radio enable
            ''')


# 服务模版关闭
def ser_disable(st_name):
    AC.send(f'''
            wlan ser {st_name}
            undo ser en
            y
            undo mlo enable
            '''
            )


# 服务模版开启
def ser_enable(st_name):
    AC.send(f'''
            wlan ser {st_name}
            mlo enable
            ser en
            
            '''
            )

# 检查MLO状态
def check_mlo_status_Activer(count):
    CheckAny("qx1240","MLO状态","dis wlan bss ap ap1 v | in MLO",["MLO status                   : Active"], count)

def check_mlo_status_Inactive(count):
    CheckAny("qx1240","MLO状态","dis wlan bss ap ap1 v | in MLO",[" MLO status                   : Inactive"], count)


def check_mlo_group_id(expect_str,count):
    AC.send(f'''
                
                
                probe
                
                '''
            )
    CheckAny("qx1240","MLO组ID","dis system internal wlan private-info ap  1 | in MLO",expect_str, count)





def main():
    while True:
        print("undo M1测试********")
        ser_disable("m1")
        time.sleep(5)
        if check_mlo_status_Activer(3) == check_mlo_group_id(['MLO GroupID1 Status                              : Unused',f'MLO GroupID2 Status                              : Used'],1):
            print("1、MLO正常")
        else:

            print("MLO状态不一致----------------------------")
            break
        print("undo M0测试********")
        ser_disable("m0")
        time.sleep(1)
        if check_mlo_status_Inactive(36) == check_mlo_group_id(['MLO GroupID1 Status                              : Unused',f'MLO GroupID2 Status                              : Unused'],1):
            print("2、MLO正常")
        else:
            print("MLO状态不一致----------------------------")
            break
        print("enable M1测试********")
        ser_enable("m1")
        time.sleep(1)
        if check_mlo_status_Activer(3) == check_mlo_group_id(['MLO GroupID1 Status                              : Used',f'MLO GroupID2 Status                              : Unused'],1):
            print("3、MLO正常")
        else:
            print("MLO状态不一致----------------------------")
            break
        print("enable M0测试********")
        ser_enable("m0")
        time.sleep(1)
        if check_mlo_status_Activer(6) == check_mlo_group_id(['MLO GroupID1 Status                              : Used',f'MLO GroupID2 Status                              : Used'],1):
            print("4、MLO正常")
        else:
            print("MLO状态不一致----------------------------")
            break
        print("radio_diable测试********")
        radio_diable()
        time.sleep(1)
        if check_mlo_status_Inactive(42) == check_mlo_group_id(['MLO GroupID1 Status                              : Unused',f'MLO GroupID2 Status                              : Unused'],1):
            print("5、MLO正常")
        else:
            print("MLO状态不一致----------------------------")
            break
        print("radio_enable测试********")
        radio_enable()
        time.sleep(1)
        if check_mlo_status_Activer(6) == check_mlo_group_id(['MLO GroupID1 Status                              : Used',f'MLO GroupID2 Status                              : Used'],1):
            print("6、MLO正常")
        else:
            print("MLO状态不一致----------------------------")
            break



if __name__ == '__main__':
    MackLog()
    main()

