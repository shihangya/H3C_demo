from function import *


def monitoring_of_buffer_pool():
    AP = connect("zhuabao")
    AP.send(f''' 

        dis ar5drv 1 statistics | inc Pool
        dis ar5drv 2 statistics | inc Pool
        dis ar5drv 3 statistics | inc Pool
    
    ''')

if __name__ == '__main__':
    while True:
        monitoring_of_buffer_pool()