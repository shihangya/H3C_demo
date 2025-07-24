from function.miji import *
import random
import string

AC = connect("anc_7538")


def generate_random_string(length):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))


def main():
    while True:
        random_string = generate_random_string(10)
        # connect_to_wifi("Z5Y5KZY9LZRS69JF","guajiceshi","123123123")
        AC.send(f'''
                        sys
                        wlan ser thd
                        undo ser enable
                        Y
                        ssid {random_string}
                        ser en
                        quit
                        quit
                        
                        ''')
        AC.send(f'''
                    sys
                    probe 
                    dis diag
                    Y
                    diag_H3C_20250723-113356.tar.gz
                    Y
                    ''')
        time.sleep(20)
        AC.send(f'''
                    quit
                    quit
                    delete flash:/diag_H3C_20250723-113356.tar.gz
                    Y
                    ''')

if __name__ == '__main__':
    main()
