from mokuai.common_imports import *

AC = connect("3520X-G")
while True:       
    add_service_template_name('ap1',['wpa3-h2e','g1','g2','g0','hsh','g3','g4','g5','g6','g7','g8','g9','g10'])
    connect_to_wifi('Z5Y5KZY9LZRS69JF',"00*h2e-V9","123123123")
    time.sleep(10)
    delete_service_template_name('ap1',['wpa3-h2e','g1','g2','g0','hsh','g3','g4','g5','g6','g7','g8','g9','g10'])