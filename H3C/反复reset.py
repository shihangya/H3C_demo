from mokuai.common_imports import *

AC = connect("3520X-G")

for i in range(1, 10):
    AC.send('''
            reset wlan client all
            Y
            ''')
    time.sleep(5)
