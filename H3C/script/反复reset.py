from mokuai.miji import *

AC = connect("wx3520x-g")

for i in range(10):
    AC.send('''
            reset wlan client all
            Y
            ''')
    time.sleep(3)
