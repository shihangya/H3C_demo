from function.miji import *
import time


AP = connect("zhuabao_copy")
while True:

    now = datetime.now().replace(microsecond=0)

    AP.send(f'''
                        
                        probe
                        dis diagnostic-information
                        Y
                        {now.strftime('%Y%m%d%H%M')}.tar.gz
                        Y
                        ''')
    time.sleep(1800)