from mokuai.common_imports import *

AC = connect("wx5560X")

for i in range(10):
    AC.send('''
            reset wlan client all
            Y
            ''')
    time.sleep(3)
