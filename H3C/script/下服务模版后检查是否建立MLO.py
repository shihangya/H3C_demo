from function.miji import *
import time


AC = connect("anc_7538")

# 通过计数器
pass_count = 0
err_count = 0

def main():
    global pass_count
    global err_count
    while True:
        AC.send('''
                    interface WLAN-Radio 1/0/1
                    ser wpa3-h2e
                    ser g0
                    ser wpa3-hnp
                    interface WLAN-Radio 1/0/2
                    ser wpa3-h2e
                    ser wpa3-hnp
                    ser g0
                    ''')
        try:
            AC.CheckCommand('是否创建MLO',
                            cmd='dis wlan bss all verbose | inc MLO status',
                            expect=['MLO status                   : Active'],
                            expect_count=4,
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
        AC.send('''
                    interface WLAN-Radio 1/0/1
                    undo ser wpa3-h2e
                    undo ser g0
                    undo ser wpa3-hnp
                    interface WLAN-Radio 1/0/2
                    undo ser wpa3-hnp
                    undo ser wpa3-h2e
                    undo ser g0

                    ''')
        time.sleep(2)




if __name__ == '__main__':
    main()
