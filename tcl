<TESTCASE_BEGIN>
<TESTCASE_HEADER_BEGIN>
<TITLE>           "IP地址学习与加密组合"
<INDEX>           "20.1.17.25.7.3_1"
<LEVEL>           "3"
<WEIGHT>          "2"
<MODULE>          "WSNP"
<TYPE>            "CMB"
<AUTHOR>          "caiyanli 15794 2018-09-30"
<LIMITATION>      "适用于无线设备"
<VERSION>         "2.1"
<DESIGN>          "1、STA配置固定IP地址，AC上配置CCMP/TKIP/WEP加密模板，STA上线后，AC和AP学习IP地址正确"
<SOURCE>          "WSNP_20.1.17.25_1.topo"
<TESTCASE_HEADER_END>

<TESTCASE_DEVICE_MAP_BEGIN>

<TESTCASE_DEVICE_MAP_END>
set ssidName1 [ CreateSSID ]
set ssidName2 [ CreateSSID ]

#wep固定地址连接命令
set wep_static_ip "am start -n com.steinwurf.adbjoinwifi/.MainActivity --esn connect -e ssid $ssidName1 -e password_type WEP -e password $wep_password -e ip $STA1IpAddress"

#ccmp固定地址连接-第一次终端上线
set wpa_static_ip "am start -n com.steinwurf.adbjoinwifi/.MainActivity --esn connect -e ssid $ssidName1 -e password_type WPA -e password $password -e ip $STA1IpAddress"
#ccmp固定地址连接-第二次终端上线
set wpa_static_ip2 "am start -n com.steinwurf.adbjoinwifi/.MainActivity --esn connect -e ssid $ssidName2 -e password_type WPA -e password $password -e ip $STA1IpAddress"




#配置RSN服务
AC1 addWlanServiceTemplate -serviceTemplate $templateNumber
#配置SSID
AC1 setSsid -serviceTemplate $templateNumber -ssidName $ssidName1
#AC上配置 TKIP加密模板
AC1 setWlanAkmMode -type  psk -serviceTemplate  $templateNumber
AC1 setWlanSecurityIe -serviceTemplate $templateNumber -type crypto - element rsn
AC1 setWlanPresharedKey -key $password -serviceTemplate $templateNumber
AC1 setWlanCipherSuite -serviceTemplate $templateNumber -type crypto -cipherSuite tkip
#使能服务模板
AC1 setServiceTemplateState -serviceTemplate $templateNumber -state $state
#将服务模板和射频绑定
AC1 addRadioServiceTemplate -apName $apName1 -model $model_num1 -radioNum $ap1_radioNum1 -templateNumber $templateNumber
#使能AP1射频
AC1 setIntfRadioState -apName $apName1 -radioNum $ap1_radioNum1 -state $state
puts "关闭WIFI"
AndroidDisconnectWirelessNetwork $udid1
AndroidDisconnectWirelessNetwork $udid1
puts "关闭成功"
<WAIT> 5
AndroidOpenWifi $udid1
puts $wpa_static_ip
<WAIT> 5


#控制##clientAP1以WAP方式上线
AndroidAdbCommandIssued $udid1 $wpa_static_ip

<WAIT> 15
AndroidPing $udid1 $addr(AC1,PORT1)
AC1 getPingDNSResolveInfo -target $STA1IpAddress
#check 1
<CHECK> description "check STA1 ping AC可以ping通"
<CHECK> type ping
<CHECK> object AC1
<CHECK> args $STA1IpAddress
<CHECK> expect 100
<CHECK> repeat 4 -interval 5
<CHECK>



#check 2
<CHECK> description "check AC1上可以学习到STA的IPv4地址"
<CHECK> type custom
<CHECK> args {
    AC1 getWlanClientIpInfo -InMacAddress $staMAC1 -ipv4Address ipv4Address
    AndroidAdbCommandIssued $udid1 $ping_STA1IpAddress
    set ipv4Addressleng [string length $ipv4Address]
    set STA1IpAddressleng [string length $STA1IpAddress]
    #            puts "ipv4Addressleng:$ipv4Addressleng \n STA1IpAddressleng:$STA1IpAddressleng"
    expr ([string equal -nocase $ipv4Address $STA1IpAddress]==1)
}
<CHECK> repeat 5 -interval 5
<CHECK> whenfailed { PUTSINFO "期望ipv4地址:$STA1IpAddress，实际ipv4地址:$ipv4Address" }
<CHECK>

#check 2.1
<CHECK> description "check AP1上可以ping通终端"
<CHECK> type ping
<CHECK> object AP1
<CHECK> args $STA1IpAddress
<CHECK> expect 100
<CHECK> repeat 5 -interval 5
<CHECK>

#check 3
<CHECK> description "check AP1上可以学习到STA的IPv4地址"
<CHECK> type custom
<CHECK> args {
    AP1 getWlanClientIpInfo -InMacAddress $staMAC1 -ipv4Address ipv4Address
    AndroidAdbCommandIssued $udid1 $ping_STA1IpAddress
    expr ([string equal -nocase $ipv4Address $STA1IpAddress]==1)
}
<CHECK> repeat 5 -interval 5
<CHECK> whenfailed { PUTSINFO "期望ipv4地址:$STA1IpAddress，实际ipv4地址:$ipv4Address" }
<CHECK>

#控制client AP下线
##clientAP1 setClientConnectState -radioIntf $clientModeIntf -action $actionDisconnect
AndroidDisconnectWirelessNetwork $udid1
AndroidDisconnectWirelessNetwork $udid1

#建立RSN服务模板
#解除radio上绑定的服务模板1
AC1 removeRadioServiceTemplate -apName $apName1 -model $model_num1  -radioNum $ap1_radioNum1 -templateNumber $templateNumber
AC1 setServiceTemplateState  -serviceTemplate $templateNumber -state $state1
#删除服务模板1
AC1 removeWlanServiceTemplate -serviceTemplate $templateNumber

#配置clear服务
AC1 addWlanServiceTemplate -serviceTemplate $templateNumber
#配置SSID
AC1 setSsid -serviceTemplate $templateNumber -ssidName $ssidName2
#AC上配置CCMP/TKIP/WEP加密模板
AC1 setWlanAkmMode -type  psk -serviceTemplate  $templateNumber
AC1 setWlanSecurityIe -serviceTemplate $templateNumber -type crypto - element rsn
AC1 setWlanPresharedKey -key $password -serviceTemplate $templateNumber
AC1 setWlanCipherSuite -serviceTemplate $templateNumber -type crypto -cipherSuite ccmp
#使能服务模板
AC1 setServiceTemplateState -serviceTemplate $templateNumber -state $state
#将服务模板和射频绑定
AC1 addRadioServiceTemplate -apName $apName1 -model $model_num1 -radioNum $ap1_radioNum1 -templateNumber $templateNumber



#打开终端WIFI
<WAIT> 5
AndroidOpenWifi $udid1
<WAIT> 20
AndroidAdbCommandIssued $udid1 $wpa_static_ip2
AndroidPing $udid1 $addr(AC1,PORT1)
AC1 getPingDNSResolveInfo -target $STA1IpAddress
AndroidPing $udid1 $addr(AC1,PORT1)
AC1 getPingDNSResolveInfo -target $STA1IpAddress

#check 4
<CHECK> description "check STA1 ping AC可以ping通"
<CHECK> type ping
<CHECK> object AC1
<CHECK> args $STA1IpAddress
<CHECK> expect 100
<CHECK> repeat 40 -interval 5
<CHECK>

#check 5
<CHECK> description "check AC1上可以学习到##clientAP1的IPv4地址"
<CHECK> type custom
<CHECK> args {
    AC1 getWlanClientIpInfo -InMacAddress $staMAC1 -ipv4Address ipv4Address
    AndroidAdbCommandIssued $udid1 $ping_STA1IpAddress
    expr ([string equal -nocase $ipv4Address $STA1IpAddress]==1)
}
<CHECK> repeat 50 -interval 5
<CHECK> whenfailed { PUTSINFO "期望ipv4地址:$STA1IpAddress，实际ipv4地址:$ipv4Address" }
<CHECK>

#check 6
<CHECK> description "check AP1上可以学习到STA的IPv4地址"
<CHECK> type custom
<CHECK> args {
    AP1 getWlanClientIpInfo -InMacAddress $staMAC1 -ipv4Address ipv4Address
    AndroidAdbCommandIssued $udid1 $ping_STA1IpAddress
    expr ([string equal -nocase $ipv4Address $STA1IpAddress]==1)
}
<CHECK> repeat 50 -interval 5
<CHECK> whenfailed { PUTSINFO "期望ipv4地址:$STA1IpAddress，实际ipv4地址:$ipv4Address" }
<CHECK>


#控制client AP下线，并清除相关配置
puts "关闭WIFI"
AndroidDisconnectWirelessNetwork $udid1
AndroidDisconnectWirelessNetwork $udid1
puts "关闭成功"

#*****************************清除配置******************************************#
#关闭radio
AC1 setIntfRadioState -apName  $apName1  -radioNum $ap1_radioNum1 -state $state2

#解除radio上绑定的服务模板1
AC1 removeRadioServiceTemplate -apName $apName1 -model $model_num1  -radioNum $ap1_radioNum1 -templateNumber $templateNumber
AC1 setServiceTemplateState  -serviceTemplate $templateNumber -state $state1

#删除服务模板1
AC1 removeWlanServiceTemplate -serviceTemplate $templateNumber

<TESTCASE_END>