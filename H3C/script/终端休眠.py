import time

from function import *

pass_count = 0
err_count = 0
AC = connect("3520h_kaoji")
def chack_MLO():
    global pass_count
    global err_count

    AC.send('''
                dis clock
                ''')
    try:
        AC.CheckCommand('是否创建MLO',
                        cmd='display wlan client verbose | inc "MLO status" ',
                        expect=['MLO status                        : Active(5G+2.4G)'],
                        expect_count=2,
                        stop_max_attempt=3,
                        relationship='and',
                        wait_fixed=3
                    )
        # 如果没有异常，说明检查通过
        pass_count += 1
        print(f"通过次数记录: {pass_count}")
        print("-" * 50)
    except Exception as e:
        print(f"检查失败: {e}")
        err_count += 1
        print(f"错误次数记录: {err_count}")
    time.sleep(5)


def main():
    while True:
        device_sleep("92232c6b")
        device_sleep("Z5Y5KZY9LZRS69JF")
        time.sleep(10)
        device_wake_up("Z5Y5KZY9LZRS69JF")
        device_wake_up("92232c6b")
        chack_MLO()



if __name__ == '__main__':
    main()




