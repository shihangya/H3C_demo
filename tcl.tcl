package provide analyze 2021.05

namespace eval ::eagle_analyze {
    variable array_log
    variable array_col_origin
    variable mem_name_origin_list ""
    variable array_col_change
    variable mem_name_change_list ""
    variable mem_change_mem_diff_list ""
    variable mem_name_no_change_list ""
    variable array_col_potential_leak
    variable mem_name_potential_leak_list ""
    variable array_col_not_potential_leak
    variable mem_name_not_potential_leak_list ""
    variable array_col_need_analyze
    variable mem_name_need_analyze_list ""
    variable count_potential_leak 0      ;#有内存泄露增长趋势列数
    variable count_not_potential_leak 0
    variable mem_busy_list ""
    variable mem_exit_list ""
    variable mem_other_list ""
    variable mem_abnormal_list ""
    variable mem_name_top_list ""
    variable mem_value_top_list ""
    variable PROCESS_NOT_EXISTS "The specified process does not exist."
    variable COMMOND_NOT_SUPPORT_VTP "-1"
    variable COMMOND_NOT_SUPPORT_TCLSH "Unrecognized command found at"
    variable USER_TYPE                  "user"
    variable TAG_TYPE                   "tag"
    variable EXTEND_TYPE                "extend"
    variable top_max 5
    variable log_file_list ""
    variable itc_excel_file_list ""
    variable scriptname [info script]
    variable array_gdefine_mid
    variable array_gdefine_mid_base
    variable itc_potential_file_list ""
    variable itc_not_potential_file_list ""

    namespace export init_eagle_analyze
    namespace export strlist_to_set
    namespace export get_log_file_list
    namespace export temp_tag_transfer
    namespace export derepeat_mem_name
    namespace export read_log_file
    namespace export analysis_busy_other_exit_mem
    namespace export analysis_abnormal_mem
    namespace export filter_no_change_mem
    namespace export analysis_potential_memory_leak
    namespace export analysis_col_potential_memory_leak
    namespace export analysis_more_top
    namespace export analyze_log_file
    namespace export get_mem_module
    namespace export print_potential_info
    namespace export get_array_gdefine_mid_base
    namespace export get_array_gdefine_mid
    namespace export analyze_user_file
    namespace export get_slot_info
    namespace export AnalyzeMemoryLeak
    namespace export get_slot_list
    namespace export check_flag_file_num
    namespace export GetUserSizeMemoryLeak
    namespace export AnalyzeResourceChange
}

proc ::eagle_analyze::init_eagle_analyze {} {
    variable array_log
    variable array_col_origin
    variable mem_name_origin_list
    variable array_col_change
    variable mem_name_change_list
    variable mem_change_mem_diff_list
    variable mem_name_no_change_list
    variable array_col_potential_leak
    variable mem_name_potential_leak_list
    variable array_col_not_potential_leak
    variable mem_name_not_potential_leak_list
    variable array_col_need_analyze
    variable mem_name_need_analyze_list
    variable count_potential_leak
    variable count_not_potential_leak
    variable mem_busy_list
    variable mem_exit_list
    variable mem_other_list
    variable mem_abnormal_list
    variable mem_name_top_list
    variable mem_value_top_list

    array unset array_log
    array set array_log {}
    array unset array_col_origin
    array set array_col_origin {}
    array unset array_col_change
    array set array_col_change {}
    array unset array_col_potential_leak
    array set array_col_potential_leak {}
    array unset array_col_not_potential_leak
    array set array_col_not_potential_leak {}
    array unset array_col_need_analyze
    array set array_col_need_analyze {}

    set mem_name_origin_list ""
    set mem_name_change_list ""
    set mem_change_mem_diff_list ""
    set mem_name_no_change_list ""
    set mem_name_potential_leak_list ""
    set mem_name_not_potential_leak_list ""
    set mem_name_need_analyze_list ""
    set count_potential_leak 0
    set count_not_potential_leak 0
    set mem_busy_list ""
    set mem_exit_list ""
    set mem_other_list ""
    set mem_abnormal_list ""
    set mem_name_top_list ""
    set mem_value_top_list ""
}

#!!================================================================
#过 程 名：  strlist_to_set
#功能类型：  ::set
#功能描述：  将给定的字符串列表转换为符合集合性质的列表:删除相同元素
#语    法：  converttoset set_list
#举    例：  set strList {abC De fg fg FG fG Fg fg}
#             puts [strlist_to_set $strList]
#             输出结果为{Fg fG FG fg De abC}
#
#参数说明：  str_set_list  集合
#返 回 值：  包含元素element的非重复列表 str_set_list
#!!================================================================
proc ::eagle_analyze::strlist_to_set { str_set_list } {
    set ele_passed {}
    set duplicate {}
    foreach e $str_set_list {
        #对元素进行统一格式处理
        set std_e $e

        #判断有无重复,删除重复元素
        if {[lsearch -exact $ele_passed $std_e]!=-1} {
            lappend duplicate $std_e
        } else {
            set set_array($e) $std_e
            lappend ele_passed $std_e
        }
    }
    set str_set_list {}
    foreach ele [array names set_array *] {
        if {[lsearch -exact $duplicate $set_array($ele)]!=-1} {
            lappend str_set_list $set_array($ele)
        } else {
            lappend str_set_list $ele
        }
    }
    return $str_set_list
}

proc ::eagle_analyze::check_flag_file_num {focus_flag user_flag tag_flag} {
    variable log_file_list
    set flag_num 0
    if {$focus_flag} {incr flag_num}
    if {$user_flag} {incr flag_num}
    if {$tag_flag} {incr flag_num}
    if {$flag_num <= [llength $log_file_list]} {
        return 1
    } else {
        return 0
    }
}

proc ::eagle_analyze::get_log_file_list {init_log_path {endfix txt}} {
    variable log_file_list

    # init_log_path为单个文件，直接返回
    set init_log_path [string trimright $init_log_path "D:/kaoji-thd/eagle-update2025/eagle_log/2025-07-17-anc_7538-777777"]
    if {[file isfile $init_log_path]} {
        lappend log_file_list $init_log_path
        return
    }

    #init_log_path为目录，遍历目录下所有文件
    set file_list [glob -nocomplain -type d "$init_log_path/*"]
    foreach sub_file $file_list {
        get_log_file_list $sub_file $endfix
    }

    set txt_file_list [glob -nocomplain "$init_log_path/*.$endfix"]
    foreach log_file $txt_file_list {
        lappend log_file_list $log_file
    }
}

proc ::eagle_analyze::get_excel_file_list {init_log_path {endfix xlsm}} {
    variable itc_excel_file_list
    
    # init_log_path为单个文件，直接返回
    set init_log_path [string trimright $init_log_path "/"]
    if {[file isfile $init_log_path]} {
        lappend itc_excel_file_list $init_log_path
        return
    }

    #init_log_path为目录，遍历目录下所有文件
    set file_list [glob -nocomplain -type d "$init_log_path/*"]
    foreach sub_file $file_list {
        get_excel_file_list $sub_file $endfix
    }

    set txt_file_list [glob -nocomplain "$init_log_path/*.$endfix"]
    foreach log_file $txt_file_list {
        lappend itc_excel_file_list $log_file        
    }
}


# 根据配置文件的slot配置，获取 slot1 slot2 的字样的板卡列表信息
proc ::eagle_analyze::get_slot_list {slot_cfg_list_str} {
    set slot_info_list ""
    set slot_cfg_list [split $slot_cfg_list_str " "]
    for {set num 0 } { $num < [ llength $slot_cfg_list ] } {incr num} {
        set slot [lindex $slot_cfg_list $num ]
        if { [string length $slot] != 0 } {
            if { [ string first - $slot ] != -1 } {
                set slot0 [ split $slot "-"]
                set chassisNo [ lindex $slot0 0]
                set slotNo [ lindex $slot0 1]
                lappend slot_info_list "chassis$chassisNo-slot$slotNo"
            } else {
                lappend slot_info_list "slot$slot"
            }
        }
    }
    return $slot_info_list
}

proc ::eagle_analyze::temp_tag_transfer {file_name} {
    variable array_log
    variable array_col_origin
    variable array_col_change
    variable mem_name_origin_list

    set log_file_id [open $file_name]
    set mem_name_origin_list ""
    while { [gets $log_file_id line_str] >= 0} {
        regsub -all {\s+}  $line_str " " line_str
        set line_str [string trim $line_str]
        if {$line_str == ""} {
            continue
        }
        if {[regexp "total" $line_str ]} {
            append mem_name_origin_list " [split $line_str " "]"
        }
    }
    set mem_name_origin_list [strlist_to_set $mem_name_origin_list]
    set mem_name_origin_list [lsort -decreasing $mem_name_origin_list]
    set mem_name_origin_list [derepeat_mem_name $mem_name_origin_list]

    close $log_file_id

    set array_log(1) $mem_name_origin_list
    set line 1
    set log_file_id [open $file_name]
    while { [gets $log_file_id line_str_name] >= 0} {
        regsub -all {\s+}  $line_str_name " " line_str_name
        set line_str [string trim $line_str_name]
        if {$line_str_name == ""} {
            continue
        }
        if {[regexp "total" $line_str_name ]} {
            set mem_name_origin_list_temp [split $line_str_name " "]
            set mem_name_origin_list_temp [derepeat_mem_name $mem_name_origin_list_temp]
            if {[gets $log_file_id line_str_number] >=0 } {
                regsub -all {\s+}  $line_str_number " " line_str_number
                set line_str [string trim $line_str_number]
                if {$line_str_number == ""} {
                    continue
                }
                set mem_origin_list_number_temp [split $line_str_number " "]
                set array_log_row ""
                foreach mem_name $mem_name_origin_list {
                    set find 0
                    set array_log_ele ""
                    for {set i 0 } {$i < [llength $mem_name_origin_list_temp]} {incr i} {
                        set mem_name_temp [lindex $mem_name_origin_list_temp $i]
                        if {$mem_name == $mem_name_temp} {
                            lappend array_col_origin($mem_name) [lindex $mem_origin_list_number_temp $i]
                            set array_log_ele [lindex $mem_origin_list_number_temp $i]
                            set find 1
                            break
                        }
                    }
                    if {!$find} {
                        lappend array_col_origin($mem_name) -1
                        set array_log_ele -1
                    }
                    lappend array_log_row $array_log_ele
                }
                incr line
                #puts array_log_row:$line:$array_log_row
                set array_log($line) $array_log_row
            }
        }
    }
    close $log_file_id

}

proc ::eagle_analyze::derepeat_mem_name {mem_mame} {
    set new_mem_name ""
    for {set i 0} {$i < [llength $mem_mame]} {incr i} {
        set ele [lindex $mem_mame $i]
        set ele [get_mem_module $ele]
        set index [lsearch $new_mem_name $ele]
        if { $index >= 0} {
            lappend new_mem_name ${ele}($i)
        } else {
            lappend new_mem_name ${ele}
        }
    }
    return $new_mem_name
}

proc ::eagle_analyze::read_log_file {file_name} {
    ::log4tcl::debug " 读取日志文件!"
    if {[regexp "temp.txt$" $file_name]} {
        temp_tag_transfer $file_name
        return
    }

    variable array_log
    variable array_col_origin
    variable array_col_change
    variable mem_name_origin_list

    set log_file_id [open $file_name]
    set line 0

    ::log4tcl::debug "从日志中获取所有内存列"
    while { [gets $log_file_id line_str] >= 0} {

        regsub -all {\s+}  $line_str " " line_str
        set line_str [string trim $line_str]
        if {$line_str == ""} {
            continue
        }
        incr line
        set array_log($line) $line_str

        if {$line == 1} {
            set mem_name_origin_list_tmp [split $line_str " "]
            #::log4tcl::debug mem_name_origin_list_tmp:$mem_name_origin_list_tmp
            set mem_name_origin_list [derepeat_mem_name $mem_name_origin_list_tmp]
            set array_log($line) [join $mem_name_origin_list " "]
        } else {
            set line_str_list [split $line_str " "]
            #puts line_str_list:$line_str_list
            for {set i 0} {$i < [llength $line_str_list]} {incr i} {
                set mem_name [lindex $mem_name_origin_list $i]
                lappend array_col_origin($mem_name) [lindex $line_str_list $i]
            }
        }
    }
    #::log4tcl::debug "mem_name_origin_list:$mem_name_origin_list"
    close $log_file_id
}

proc ::eagle_analyze::analysis_busy_other_exit_mem {} {
    ::log4tcl::debug " 获取处于忙碌，退出及其他状态的内存列表!"

    variable array_col_change
    variable mem_name_change_list
    variable mem_other_list
    variable mem_exit_list
    variable mem_busy_list
	variable mem_abnormal_list

    set log_file_col_count [llength $mem_name_change_list]
    for {set i 0} {$i < $log_file_col_count} {incr i} {
        set mem_name [lindex $mem_name_change_list $i]
        set col_change_list $array_col_change($mem_name)
        if {[lsearch $col_change_list -1] >=0 } {
            lappend mem_other_list $mem_name
        }
        if {[lsearch $col_change_list -2] >=0 } {
            lappend mem_exit_list $mem_name
        }
        if {[lsearch $col_change_list -3] >=0 } {
            lappend mem_busy_list $mem_name
        }
		set zero_num 0
		set nega_num 0
		foreach j $col_change_list {
			if {$j < 0} {
				incr nega_num
			}
			if {$j == 0} {
				incr zero_num
			}
		}
		if { $nega_num >= [llength $col_change_list]*0.5 || $zero_num >= [llength $col_change_list]*0.5} {
            lappend mem_abnormal_list $mem_name
		}
    }
}

proc ::eagle_analyze::analysis_abnormal_mem {} {
    ::log4tcl::debug " 获取Tag进程一直为0或者一直为-1的内存列表!"
	
	variable array_col_origin
    variable mem_name_no_change_list
	variable mem_abnormal_list

    set log_file_col_count [llength $mem_name_no_change_list]
    for {set i 0} {$i < $log_file_col_count} {incr i} {
        set mem_name [lindex $mem_name_no_change_list $i]
        set col_origin_list $array_col_origin($mem_name)
		set zero_num 0
		set nega_num 0
		# ::log4tcl::debug "col_origin_list     : $col_origin_list"
		if {[lsearch $col_origin_list -1] >=0 || [lsearch $col_origin_list 0] >=0} {
            lappend mem_abnormal_list $mem_name
        }
    }
}

#!!================================================================
#过 程 名：  filter_no_change_mem
#功能描述：  从日志中筛选出内存有变化的列，及无变化的列
#!!================================================================
proc ::eagle_analyze::filter_no_change_mem {} {
    ::log4tcl::debug " 获取没有变化的内存列表!"
    variable array_col_origin
    variable array_col_change
    variable mem_name_origin_list
    variable mem_name_no_change_list
    variable mem_name_change_list

    for {set col 0} {$col < [llength $mem_name_origin_list]} {incr col} {
        set mem_name [lindex $mem_name_origin_list $col]
        if {[llength [strlist_to_set $array_col_origin($mem_name)]] > 1} {
            lappend mem_name_change_list $mem_name
            set array_col_change($mem_name) $array_col_origin($mem_name)
            #::log4tcl::debug $mem_name:$array_col_change($mem_name)
        } else {
            lappend mem_name_no_change_list $mem_name
        }
    }
    #::log4tcl::debug mem_name_no_change_list:$mem_name_no_change_list
}

#!!================================================================
#过 程 名：  analysis_potential_memory_leak
#功能描述：  计算可能有内存泄露，不大可能有内存泄露及需要人手工分析的数据
#计算公式：  可能有内存泄露：每5行一个区段，每个区段的最大值最小值都比上一个区段大的数目 > 区段数* 0.8，
#                            30行以内的数据，需要全部连续递增
#            不太可能有内存泄露：每5行一个区段，每个区段的最大值最小值与上一个区段相同的数目 > 区段数* 0.6
#            待分析：内存有变化-可能有内存泄露-不太可能有内存泄露
#返 回 值：  可能有内存泄露     1
#            不太可能有内存泄露 2
#            待分析             3
#!!================================================================
proc ::eagle_analyze::analysis_potential_memory_leak {} {

    variable count_potential_leak
    variable count_not_potential_leak
    variable array_col_change
    variable mem_name_change_list
    variable array_col_potential_leak
    variable mem_name_potential_leak_list
    variable array_col_not_potential_leak
    variable mem_name_not_potential_leak_list
    variable array_col_need_analyze
    variable mem_name_need_analyze_list
    set mem_name_need_analyze_diff_list ""

    ::log4tcl::debug mem_name_change_list:$mem_name_change_list
    for {set col 0} {$col < [llength $mem_name_change_list]} {incr col} {
        set mem_name [lindex $mem_name_change_list $col]
        set mem_col_change_list $array_col_change($mem_name)
        set result [analysis_col_potential_memory_leak "$mem_col_change_list"]
        switch $result  {
            1 {
                lappend mem_name_potential_leak_list $mem_name
                set array_col_potential_leak($mem_name) $mem_col_change_list
                incr count_potential_leak
            }
            2 {
                lappend mem_name_not_potential_leak_list $mem_name
                set array_col_not_potential_leak($mem_name) $mem_col_change_list
                incr count_not_potential_leak
            }
            0 {
                #lappend mem_name_need_analyze_list $mem_name
                set diff [expr [lindex $mem_col_change_list end] - [lindex $mem_col_change_list 0]]
                if {$diff < 0} {set diff 0}
                lappend mem_name_need_analyze_diff_list "[format %012d $diff]@$mem_name"
                set array_col_not_potential_leak($mem_name) $mem_col_change_list
            }
        }

        if {$count_potential_leak > 100} {
            ::log4tcl::error "持续增长趋势的列数超过了100，数据异常，请确认！"
            set beAbnormal 1
            return 0
        }
    }

    set mem_name_need_analyze_diff_sort_list [lsort -decreasing $mem_name_need_analyze_diff_list]
    foreach mem_diff $mem_name_need_analyze_diff_sort_list {
        lappend mem_name_not_potential_leak_list [string range $mem_diff [expr [string first @ $mem_diff]+1] end]
    }

    ::log4tcl::debug "可能存在内存泄露列表     : $mem_name_potential_leak_list"
    ::log4tcl::debug "不大可能存在内存泄露列表 : $mem_name_not_potential_leak_list"
    ::log4tcl::debug "待分析列表                : $mem_name_need_analyze_list"

    return 1
}

proc ::eagle_analyze::analysis_col_potential_memory_leak {mem_col_change_list} {
    set count_seg_increase 0
    set count_seg_sum_increase 0
    set count_seg_ava_increase 0
    set count_seg_calm 0
    set change_count [llength $mem_col_change_list]
    set intSeg [expr $change_count/5]
    

    #对于3-9轮的数据,完全递增认为有可能有内存泄露
    if {$change_count <= 9 && $change_count >=3} {
        set mem_num_init [lindex $mem_col_change_list 0]
        for {set i 1} {$i < [llength $mem_col_change_list]} {incr i} {
            set mem_num [lindex $mem_col_change_list $i]
            if {$mem_num <= $mem_num_init} {
                return 0
            }
            set mem_num_init $mem_num
        }
        return 1
    }

    #对于大于等于10轮的数据
    array unset lngMin ;#列各区段的最小值
    array unset lngMax ;#列各区段的最大值
    array unset lngAvarage ;#列各区段的均值
    array unset lngSum     ;#列各区段的均值
    for {set i 0} {$i < $intSeg} {incr i} {
        set seg_mem_col_change_list [lrange $mem_col_change_list [expr $i * 5] [expr ($i+1) * 5 - 1] ]
        set seg_mem_col_change_sort_list [lsort -real -decreasing $seg_mem_col_change_list]
        set lngMax($i) [lindex $seg_mem_col_change_sort_list 0]
        set lngMin($i) [lindex $seg_mem_col_change_sort_list end]

        # 去掉一个最大值，去掉一个最小值，取总和，持续增加的才算
        set lngSumx 0
        set sunNum 0
        for {set x 0} {$x < [llength $seg_mem_col_change_list]} {incr x} {
            set mem_col [lindex $seg_mem_col_change_list $x]
            if {$mem_col > 0 } {
                incr lngSumx [lindex $seg_mem_col_change_list $x]
                incr sunNum
            }
        }
        if {$lngSumx > 0 } {
            set lngAvarage($i) [expr $lngSumx/$sunNum]
        } else {
            set lngAvarage($i) 0
        }

        set lngSumx 0
        for {set x 1} {$x < [llength $seg_mem_col_change_list]-1} {incr x} {
            incr lngSumx [lindex $seg_mem_col_change_list $x]
        }
        set lngSum($i) $lngSumx
        #::log4tcl::debug lngMax:$lngMax($i)
        #::log4tcl::debug lngMin:$lngMin($i)
        if {$i > 0 } {
            if {$lngMax($i) > $lngMax([expr $i - 1]) && $lngMin($i) > $lngMin([expr $i - 1]) } {
                incr count_seg_increase
            }

            if {$lngMax($i) == $lngMax([expr $i - 1]) && $lngMin($i) == $lngMin([expr $i - 1]) } {
                incr count_seg_calm
            }

            if {$lngAvarage($i) > $lngAvarage([expr $i - 1])} {
                incr count_seg_ava_increase
            }

            if {$lngSum($i) > $lngSum([expr $i - 1])} {
                incr count_seg_sum_increase
            }
        }
    }

    ::log4tcl::debug count_seg_increase:$count_seg_increase
    ::log4tcl::debug count_seg_calm:$count_seg_calm
    ::log4tcl::debug intSeg:$intSeg

    if {$count_seg_increase > 0 && ($count_seg_increase == [expr $intSeg - 1] || $count_seg_increase > [expr $intSeg * 0.8])} {
        return 1
    }

    if {$intSeg > 0 && $count_seg_calm > $intSeg * 0.6} {
        return 2
    }

    #如果总和也持续增加，则认为有可能有内存泄露
    if {$count_seg_sum_increase > 1 && ($count_seg_sum_increase == [expr $intSeg - 1] || $count_seg_sum_increase > [expr $intSeg * 0.7])} {
        return 1
    }

    #如果平均值也持续增加，则认为有可能有内存泄露
    if {$count_seg_ava_increase > 1 && ($count_seg_ava_increase == [expr $intSeg - 1] || $count_seg_ava_increase > [expr $intSeg * 0.7])} {
        return 1
    }

    #如果平均值持续增加，则认为有可能有内存泄漏
    if ($count_seg_ava_increase == [expr $intSeg - 1] || $count_seg_ava_increase > [expr $intSeg * 0.7])} {
        return 1
    }

    return 0
}

proc ::eagle_analyze::analysis_more_top {} {
    variable top_max
    variable mem_name_potential_leak_list

    ::log4tcl::debug " 获取内存增长 TOP 列表"

    variable array_col_change
    variable mem_change_mem_diff_list
    variable array_col_top
    variable mem_name_origin_list
    variable mem_name_top_list
    variable mem_value_top_list

    ::log4tcl::debug "获取待分析数据表各列的内存差值"
    #foreach {key value} [array get array_col_change]
    foreach key $mem_name_potential_leak_list {
        set max_v [lindex [lsort -integer -decreasing $array_col_change($key)] 0]
        set min_v [lindex [lsort -integer -decreasing $array_col_change($key)] end]
        lappend mem_change_mem_diff_list [expr $max_v - $min_v]
    }

    ::log4tcl::debug "内存增长 TOP5 列表:"
    #set col_title [array names array_col_change]
    set col_title $mem_name_potential_leak_list
    set col_value $mem_change_mem_diff_list

    set max_v [lindex [lsort -integer -decreasing $col_value] 0]
    set min_v [lindex [lsort -integer -decreasing $col_value] end]

    set value_title_list ""
    foreach value $col_value title $col_title {
        lappend value_title_list "$value $title"
    }

    if {$value_title_list != ""} {
        set sorted_value_title_list [lsort -decreasing -dictionary $value_title_list]
        set sorted_value_title_list_len [llength $sorted_value_title_list]
        set topnum 0
        if { $sorted_value_title_list_len >= $top_max+1 } {
            for {set i 0} {$i < $top_max+1} {incr i} {
                set value [lindex [lindex $sorted_value_title_list $i] 0]
                if {$value != 0} {
                    #第一列不参与topo计算
                    if { [lindex [lindex $sorted_value_title_list $i] 1] == [lindex $mem_name_origin_list 0]} {
                        continue
                    }
                    lappend mem_name_top_list [lindex [lindex $sorted_value_title_list $i] 1]
                    lappend mem_value_top_list $value
                    ::log4tcl::debug "TOP [incr topnum] : [lindex [lindex $sorted_value_title_list $i] 1] ( $value )"
                }
            }
        } else {
            for {set i 0} {$i < $sorted_value_title_list_len } {incr i} {
                set value [lindex [lindex $sorted_value_title_list $i] 0]
                if {$value != 0} {
                    #第一列不参与topo计算
                    if { [lindex [lindex $sorted_value_title_list $i] 1] == [lindex $mem_name_origin_list 0]} {
                        continue
                    }
                    lappend mem_name_top_list [lindex [lindex $sorted_value_title_list $i] 1]
                    lappend mem_value_top_list $value
                    ::log4tcl::debug "TOP [incr topnum]: [lindex [lindex $sorted_value_title_list $i] 1] ( $value )"
                }
            }
        }
    }
}

proc ::eagle_analyze::analyze_log_file_potential {log_file_path} {
    catch {
        ::log4tcl::step " 清空上一个文件数据!"
        init_eagle_analyze

        ::log4tcl::step " 读取日志文件! $log_file_path"
        read_log_file $log_file_path

        ::log4tcl::step " 获取没有变化的内存列表!"
        filter_no_change_mem

        ::log4tcl::step " 分析可能存在内存泄露进程!"
        analysis_potential_memory_leak

    } errormsg
}

proc ::eagle_analyze::analyze_log_file { log_file_path {need_excel_list 0} {init_log_dir "" }  \
            {all_potential_focus_list_out "" } {all_potential_tag_list_out ""} \
            {all_potential_user_list_out "" } {all_potential_file_list_out "" } {all_potential_handle_list_out "" } \
            {all_potential_slabinfo_list_out ""} {all_potential_vmallocinfo_list_out ""} \
            {all_potential_log_list_out "" } {all_potential_user_size_list_out ""} {all_potential_tag_size_list_out ""}} {
    variable mem_name_potential_leak_list
    catch {
        analyze_log_file_potential $log_file_path

        ::log4tcl::step " 获取处于忙碌，退出及其他状态的内存列表!"
        analysis_busy_other_exit_mem
		
		::log4tcl::step " 获取tag进程一直为0或者一直为-1的内存列表!"
		analysis_abnormal_mem

        ::log4tcl::step " 获取内存增长TOP列表"
        analysis_more_top

        if {$need_excel_list && $mem_name_potential_leak_list != ""} {
            upvar $all_potential_user_list_out all_potential_user_list_in
            upvar $all_potential_user_size_list_out all_potential_user_size_list_in
            upvar $all_potential_tag_list_out all_potential_tag_list_in
            upvar $all_potential_tag_size_list_out all_potential_tag_size_list_in
            upvar $all_potential_focus_list_out all_potential_focus_list_in
            upvar $all_potential_file_list_out all_potential_file_list_in
            upvar $all_potential_handle_list_out all_potential_handle_list_in
            upvar $all_potential_slabinfo_list_out all_potential_slabinfo_list_in
            upvar $all_potential_vmallocinfo_list_out all_potential_vmallocinfo_list_in
            upvar $all_potential_log_list_out all_potential_log_list_in
            set file_name $log_file_path
            regsub "$init_log_dir/" $file_name "" file_name
            set file_name_no_txt [string range $file_name 0 end-4]
            set excel_file_name $file_name_no_txt.xlsm
            lappend all_potential_log_list_in "$log_file_path"

            if {[regexp user.txt$ $file_name]} {
                lappend all_potential_user_list_in "$excel_file_name"
                lappend all_potential_user_list_in "$mem_name_potential_leak_list"
            } elseif {[regexp user-.*.txt$ $file_name]} {
                lappend all_potential_user_size_list_in "$excel_file_name"
                lappend all_potential_user_size_list_in "$mem_name_potential_leak_list"
            } elseif {[regexp focus.txt$ $file_name]} {
                lappend all_potential_focus_list_in "$excel_file_name"
                lappend all_potential_focus_list_in "$mem_name_potential_leak_list"
            } elseif {[regexp tag.txt$ $file_name]} {
                lappend all_potential_tag_list_in "$excel_file_name"
                lappend all_potential_tag_list_in "$mem_name_potential_leak_list"
            } elseif {[regexp tag-.*.txt$ $file_name]} {
                lappend all_potential_tag_size_list_in "$excel_file_name"
                lappend all_potential_tag_size_list_in "$mem_name_potential_leak_list"
            } elseif {[regexp temp.txt$ $file_name]} {
                lappend all_potential_tag_list_in "$excel_file_name"
                lappend all_potential_tag_list_in "$mem_name_potential_leak_list"
            } elseif {[regexp filecheck.txt$ $file_name]} {
                lappend all_potential_file_list_in "$excel_file_name"
                lappend all_potential_file_list_in "$mem_name_potential_leak_list"
            } elseif {[regexp handle.txt$ $file_name]} {
                lappend all_potential_handle_list_in "$excel_file_name"
                lappend all_potential_handle_list_in "$mem_name_potential_leak_list"
            } elseif {[regexp slabinfo.txt$ $file_name]} {
                lappend all_potential_slabinfo_list_in "$excel_file_name"
                lappend all_potential_slabinfo_list_in "$mem_name_potential_leak_list"
            } elseif {[regexp vmallocinfo.txt$ $file_name]} {
                lappend all_potential_vmallocinfo_list_in "$excel_file_name"
                lappend all_potential_vmallocinfo_list_in "$mem_name_potential_leak_list"
            }
        }
    } errormsg

    #if {$errormsg != ""} {
    #::log4tcl::error "analyze_log_file_errormsg: $errormsg"
    #}
}

proc ::eagle_analyze::confLine {str num } {
    set line $str
    set length [ string length $str ]
    while { $length < $num } {
        append line " "
        incr length 1
    }
    return $line
}

proc ::eagle_analyze::print_potential_info { terminal_name all_potential_list init_log_dir excel_auto_open current_count_out {all_potential_size_list ""}} {
    set slot_info_list ""
    upvar $current_count_out current_count_in
    foreach {filename mem_name} $all_potential_list {
        lappend slot_info_list [get_excel_slot_info $filename]
    }
    set slot_info_list [lsort [strlist_to_set $slot_info_list]]
    set lipc_analyze 0
    set total_count 0
    foreach slot_info $slot_info_list {
        foreach {filename mem_name} $all_potential_list {

            # 多级目录处理
            set log_dir [file dir $init_log_dir/$filename]
            set file_pre_dir ""
            regexp {/([^/]+)$} $log_dir match file_pre_dir
            if {$file_pre_dir!= ""} {append file_pre_dir -}
            set filename [file tail $init_log_dir/$filename]

            set slot_info_in [get_excel_slot_info $filename]
            if {$slot_info_in == $slot_info} {

                set pre_info "$terminal_name"
                if {$slot_info != ""} {
                    set pre_info "$terminal_name-$slot_info"
                }
                set file_name_no_txt [string range $filename 0 end-5]

                if { [ expr [regexp tag $filename] || [regexp user $filename] || [regexp focus $filename]] == 0} {
                    incr current_count_in
                    if {$current_count_in != 1} {
                        ::log4tcl::info ""
                    }
                    ::log4tcl::info "    $current_count_in、$pre_info ($mem_name)"
                    if {$excel_auto_open} {
                        ::log4tcl::info "           内存增长曲线见已打开Excel文件 ：${file_pre_dir}$filename，点击内存泄露分析按钮"
                    } else {
                        ::log4tcl::info "           内存增长曲线见                ：$log_dir/${file_pre_dir}$filename"
                    }
                    set log_file_list [glob -nocomplain "$log_dir/$file_name_no_txt-trace-*.log"]
                    if {$log_file_list !="" && [regexp user $file_name_no_txt]} {
                        ::log4tcl::info     "           各模块泄露的初步定位记录见    ：$log_dir/$file_name_no_txt-trace-*.log"
                    }
                }
            }

            set file_name_tail [file tail $filename]
            set file_name_no_txt [string range $file_name_tail 0 end-5]
            set find_size 0
            foreach {size_file_name size_name} $all_potential_size_list {
                if {[regexp "$file_name_no_txt-" $size_file_name]} {
                    set size_slot_info_in [get_excel_slot_info $size_file_name]
                    if {$size_slot_info_in == $slot_info} {
                        set find_size 1
                        set size_file_name_tail [file tail $size_file_name]
                        set size_file_name_no_txt [string range $size_file_name_tail 0 end-5]
                        regsub $slot_info $size_file_name_no_txt "" size_file_name_no_txt_no_slot
                        incr current_count_in
                        if {$current_count_in != 1} {
                            ::log4tcl::info ""
                        }

                        ::log4tcl::info "    $current_count_in、$pre_info-$size_file_name_no_txt_no_slot模块-size ($size_name)"
                        if {$excel_auto_open} {
                            ::log4tcl::info "      Size增长曲线见已打开Excel文件 ：${file_pre_dir}$size_file_name，点击内存泄露分析按钮"
                        } else {
                            ::log4tcl::info "      Size增长曲线见                ：$log_dir/${file_pre_dir}$size_file_name"
                        }

                        #LIPC模块进一步分析
                        if {[regexp "0x10b0000" $size_file_name_no_txt_no_slot]} {
                            get_lipc_detail_info $slot_info
                        }

                        regsub {([^-]+)$} $size_file_name_no_txt "trace-\\1" size_file_name_no_txt_tmp
                        if {[file isfile "$log_dir/${size_file_name_no_txt_tmp}.log"]} {
                            ::log4tcl::info     "      模块泄露的初步定位记录见      ：$log_dir/${size_file_name_no_txt_tmp}.log"
                        }
                    }
                }
            }
        }
    }
}

#!!================================================================
#过 程 名：  get_mem_module
#功能描述：  获取内核态内存与子模块的对应关系
#!!================================================================
proc ::eagle_analyze::get_mem_module {mem_name} {
    variable array_gdefine_mid
    set mem_module ""
    catch {
        #非内核态内存，直接返回
        if {0 == [regexp 0x $mem_name]} {
            set mem_module $mem_name
        } else {

            set len_mem_name [llength $mem_name]
            set mem_name [string tolower $mem_name]
            if {$len_mem_name < 10} {
                regsub 0x $mem_name 0x0 tem_mem_name
            }
            set mem_name_pre_six [string range $tem_mem_name 2 5]
            if { [info exists array_gdefine_mid($mem_name_pre_six)] } {
                set mem_module ${mem_name}($array_gdefine_mid($mem_name_pre_six))
            } else {
                set mem_module $mem_name
            }
        }
    } erromsg
    #::log4tcl::debug get_mem_module_erromsg:$erromsg
    return $mem_module
}

proc ::eagle_analyze::get_array_gdefine_mid_base {} {

    variable scriptname
    variable array_gdefine_mid_base
    catch {
        set gdefine_mid_base_file "[file dir $scriptname]/resource/gdefine_mid_base.conf"
        set gdefine_mid_base_file_id [open $gdefine_mid_base_file]
        while {[gets $gdefine_mid_base_file_id line_str] >=0} {
            set mid_base_name ""
            set mid_base_hex ""
            if {[regexp {#define\s*(\w+)\s*0x(\w{2})} $line_str match mid_base_name mid_base_hex]} {
                if {$mid_base_name != "" && $mid_base_hex != ""} {
                    #::log4tcl::debug $mid_base_name:$mid_base_hex
                    set array_gdefine_mid_base($mid_base_name) $mid_base_hex
                }
            }
        }
        close $gdefine_mid_base_file_id
    } erromsg

    ::log4tcl::debug get_array_gdefine_mid_base_erromsg:$erromsg
}

#define  MID_INPCB                      MID_DEFINE(MID_WAN_BASE, 0x0D)
proc ::eagle_analyze::get_array_gdefine_mid {} {
    variable scriptname
    variable array_gdefine_mid
    variable array_gdefine_mid_base
    catch {
        set gdefine_mid_file "[file dir $scriptname]/resource/gdefine_mid.conf"
        set gdefine_mid_file_id [open $gdefine_mid_file]
        while {[gets $gdefine_mid_file_id line_str] >=0} {
            set mid_base_name ""
            set mid_name ""
            set mid_hex ""
            if {[regexp {#define\s*(\w+)\s*MID_DEFINE\((\w+), 0x(\w{2})\)} $line_str match mid_name mid_base_name mid_hex]} {
                if {$mid_name != "" && $mid_base_name != "" && $mid_hex != ""} {
                    set mid_hex_four "[string tolower $array_gdefine_mid_base($mid_base_name)$mid_hex]"
                    #::log4tcl::debug $mid_hex_four:[string range [string tolower $mid_name] 4 end]
                    set array_gdefine_mid($mid_hex_four) [string range [string tolower $mid_name] 4 end]
                }
            }
        }
        close $gdefine_mid_file_id
    } erromsg

    ::log4tcl::debug get_array_gdefine_mid_erromsg:$erromsg
}

proc ::eagle_analyze::get_slot_info {log_file_path} {
    set slotinfo ""

    if {[regexp {chassis(\d+)-slot(\d+)-cpu(\d+)-.*\.txt} $log_file_path match chassis slot cpu]} {
        set slotinfo $chassis-$slot-$cpu
        return $slotinfo
    }

    if {[regexp {chassis(\d+)-slot(\d+)-.*\.txt} $log_file_path match chassis slot]} {
        set slotinfo $chassis-$slot
        return $slotinfo
    }

    if {[regexp {slot(\d+)-.*\.txt} $log_file_path match slot]} {
        set slotinfo $slot
        return $slotinfo
    }
    return $slotinfo
}

proc ::eagle_analyze::get_excel_slot_info {log_file_path} {
    set slotinfo ""
    if {[regexp {(chassis\d+-slot\d+-cpu\d+)-} $log_file_path match slot]} {
        set slotinfo $slot
    } elseif {[regexp {(chassis\d+-slot\d+)-} $log_file_path match slot]} {
        set slotinfo $slot
    } elseif {[regexp {(slot\d+)-} $log_file_path match slot]} {
        set slotinfo $slot
    }
    return $slotinfo
}

proc ::eagle_analyze::GetUserSizeMemoryLeak {init_log_path commandLine sysname} {
    #分析用户态内存泄露，得到详细的Size变化
    set ::eagle_analyze::log_file_list ""
    ::eagle_analyze::get_log_file_list "$init_log_path"
    set log_count [llength $::eagle_analyze::log_file_list]
    set log_file_potential_all_list ""
    set mem_name_potential_leak_all_list ""
    set log_file_type_list ""

    for {set i 0} {$i < $log_count} {incr i} {
        set log_file_path [lindex $::eagle_analyze::log_file_list $i]
        ::log4tcl::setstepindex 1

        # 分析日志文件
        ::eagle_analyze::analyze_log_file_potential $log_file_path

        # 获取文件类型
        set log_file_type ""
        if {[string last user.txt $log_file_path] > 0} {
            set log_file_type "$::eagle_analyze::USER_TYPE"
        } elseif {[string last tag.txt $log_file_path] > 0} {
            set log_file_type "$::eagle_analyze::TAG_TYPE"
        } else {
            set log_file_type "$::eagle_analyze::EXTEND_TYPE"
            #只处理用户态和tag态的进一步详细数据
            continue;
        }

        # 追加所有的泄露字段列表
        if {$::eagle_analyze::mem_name_potential_leak_list != ""} {
            foreach mem_name $::eagle_analyze::mem_name_potential_leak_list {
                if {$mem_name != "total"} {
                    lappend log_file_potential_all_list $log_file_path
                    lappend mem_name_potential_leak_all_list $mem_name
                    lappend log_file_type_list $log_file_type
                }
            }
        }
    }

    if {[llength $mem_name_potential_leak_all_list] > 0} {
        ::log4tcl::info "     开始获取疑似泄露模块的详细字节块... "
        GetMemoryDetailSize $log_file_potential_all_list $mem_name_potential_leak_all_list $log_file_type_list $commandLine $sysname
    }
}

# 根据用户设置的cpu阈值，获取display memory-cpu history 最近的值
proc ::eagle_analyze::getNearCpuRate {ratio} {
    regsub {\.*} $ratio "" ratio
    regsub {%} $ratio "" ratio
    if  {$ratio <= 5} {
        return $ratio
    } elseif {$ratio <= 7} {
        return "5"
    } elseif {$ratio <= 10} {
        return "10"
    } elseif {$ratio <= 100} {
        set ratio_end [string range $ratio end end]
        set ratio_pre [string range $ratio 0 end-1]
        if {$ratio_end <=2} {
            return "${ratio_pre}0"
        } elseif {$ratio_end <=5} {
            return "${ratio_pre}5"
        } elseif {$ratio_end <=7} {
            return "[expr ${ratio_pre}]5"
        } else {
            return "[expr ${ratio_pre} + 1]0"
        }
    } else {
        return "100"
    }
}

proc ::eagle_analyze::AnalyzeCpuHistory {init_log_path cpu_ratio array_max_cpu_usage} {
    if {$cpu_ratio== ""} {
        return 0
    }
    set cfg_cpu_ratio [getNearCpuRate $cpu_ratio]
    upvar $array_max_cpu_usage array_max_cpu_usage_in
    set slot_list [array names array_max_cpu_usage_in]
    ::log4tcl::info "开始分析CPU历史使用情况... "
    set count 0

    foreach slot $slot_list {
        set max_cpu_usage_list $array_max_cpu_usage_in($slot)
        set slot_info ""
        set slot_info_infile ""
        if {$slot != ""} {
            set slot_info [::eagle_function::GetSlotInfoInCommand $slot]
            set slot_info_infile [::eagle_function::GetSlotInfoInFile $slot]
        }

        for {set i 0} {$i < [llength $max_cpu_usage_list]} {incr i} {
            set max_cpu_usage [lindex $max_cpu_usage_list $i]

            if {$max_cpu_usage >= $cfg_cpu_ratio} {
                ::log4tcl::info "    $slot_info第 [expr $i+1] 次获取的最大CPU使用率 $max_cpu_usage 达到脚本设置阈值 $cpu_ratio。"
                ::log4tcl::info "    CPU历史使用率记录详见文件：$init_log_path/${slot_info_infile}cpu.log"
                incr count
                break
            }
        }
    }

    if {$count == 0} {
        ::log4tcl::info "CPU历史使用情况总体分析结论: 未发现CPU异常情况。"
    }

    return $count
}

proc ::eagle_analyze::AnalyzeMemoryLeak {terminal_name init_log_path excel_auto_open write_not_potential} {
    namespace import ::eagle_excel::*
    variable itc_potential_file_list ""
    variable itc_not_potential_file_list ""

    #遍历指定目录，获取日志文件列表
    get_excel_col_list
    set ::eagle_analyze::log_file_list ""
    set ::eagle_analyze::itc_excel_file_list ""
    get_log_file_list "$init_log_path"
    get_array_gdefine_mid_base
    get_array_gdefine_mid

    set log_count [llength $::eagle_analyze::log_file_list]
    set all_potential_focus_list ""
    set all_potential_tag_list ""
    set all_potential_user_list ""
    set all_potential_file_list ""
    set all_potential_handle_list ""
    set all_potential_slabinfo_list ""
    set all_potential_vmallocinfo_list ""
    set all_potential_user_size_list ""
    set all_potential_log_list ""
    set all_potential_num 0

    ::log4tcl::info "开始分析内存记录文件，并生成有可能有内存泄露的Excel文件... "
    #遍历日志文件，生成分析结果
    for {set i 0} {$i < $log_count} {incr i} {

        set log_file_path [lindex $::eagle_analyze::log_file_list $i]
        ::log4tcl::setstepindex 1

        # 分析日志文件
        set all_potential_tag_size_list ""
        set all_potential_user_size_list ""
        analyze_log_file $log_file_path 1 $init_log_path all_potential_focus_list all_potential_tag_list all_potential_user_list all_potential_file_list all_potential_handle_list all_potential_slabinfo_list all_potential_vmallocinfo_list all_potential_log_list all_potential_user_size_list all_potential_tag_size_list
        # 有内存泄露时，写Excel文件
        if {$::eagle_analyze::mem_name_potential_leak_list != ""} {
            if {$::eagle_function::detail_size == 0} {
		incr all_potential_num [llength $::eagle_analyze::mem_name_potential_leak_list ]
	    } elseif {!([regexp user.txt$ $log_file_path]|| [regexp tag.txt$ $log_file_path])} {
                incr all_potential_num [llength $::eagle_analyze::mem_name_potential_leak_list ]
            }
            ::log4tcl::info "    [expr $i+1]、$log_file_path 疑似有内存泄露，开始生成Excel文件"
            lappend itc_potential_file_list $log_file_path
            set create_result [create_excel_file $log_file_path $excel_auto_open]
            if {$create_result == 0} {
                ::log4tcl::error "$log_file_path 生成Excel失败"
            }
        } else {
            ::log4tcl::info "    [expr $i+1]、$log_file_path 无明确内存泄露"
            lappend itc_not_potential_file_list $log_file_path
        }
    }

    if {$all_potential_num == 0} {
        ::log4tcl::info "\n内存记录文件总体分析结论: 未发现内存泄露模块。"
    } else {
        ::log4tcl::info "\n内存记录文件总体分析结论: 有 $all_potential_num 个模块 $::eagle_analyze::mem_name_potential_leak_list 可能存在内存泄露，请分析确认... "
    }
    set current_count 0
    if {$all_potential_focus_list != ""} {
        print_potential_info $terminal_name $all_potential_focus_list $init_log_path $excel_auto_open current_count ""
    }

    if {$all_potential_user_list != ""} {
        print_potential_info $terminal_name $all_potential_user_list $init_log_path $excel_auto_open current_count $all_potential_user_size_list
    }

    if {$all_potential_tag_list != ""} {
        print_potential_info $terminal_name $all_potential_tag_list $init_log_path $excel_auto_open current_count $all_potential_tag_size_list
    }

    if {$all_potential_file_list != ""} {
        print_potential_info $terminal_name $all_potential_file_list $init_log_path $excel_auto_open current_count ""
    }

    if {$all_potential_handle_list != ""} {
        print_potential_info $terminal_name $all_potential_handle_list $init_log_path $excel_auto_open current_count ""
    }
   
    if {$all_potential_slabinfo_list != ""} {
        print_potential_info $terminal_name $all_potential_slabinfo_list $init_log_path $excel_auto_open current_count ""
    }
    
    if {$all_potential_vmallocinfo_list != ""} {
        print_potential_info $terminal_name $all_potential_vmallocinfo_list $init_log_path $excel_auto_open current_count ""
    }

    if {$write_not_potential} {
        ::log4tcl::info "\n开始生成无明确内存泄露日志的excel数据，如果不需要可以修改config.tcl中参数write_not_potential。"
        for {set i 0} {$i < $log_count} {incr i} {
            set log_file_path [lindex $::eagle_analyze::log_file_list $i]
            ::log4tcl::setstepindex 1
            if {[lsearch $all_potential_log_list $log_file_path] < 0} {
                analyze_log_file $log_file_path
                create_excel_file $log_file_path
            }
        }
    }
    #生成excel文件后，用于记录excel文件路径
    get_excel_file_list "$init_log_path"
    return $all_potential_num
}

#总共下发10次拷机命令版本，获取用户态和tag态更详细的内存泄露数据
proc ::eagle_analyze::GetMemoryDetailSize {log_file_potential_list mem_name_potential_leak_all_list log_file_type_list cmd_list sysname} {
    variable PROCESS_NOT_EXISTS
    variable COMMOND_NOT_SUPPORT_VTP
    variable COMMOND_NOT_SUPPORT_TCLSH

    # 预处理后保留的需要获取详细数据的变量
    set slot_info_in_command_list ""
    set slot_info_list ""
    set job_id_list ""
    set job_name_list ""
    set job_type_list ""
    set log_file_list ""

    # 汇总需要获取详细内存的用户态jobid 和 tag态tag，避免每个板卡下发10次，提高效率
    foreach log_file_path $log_file_potential_list mem_name $mem_name_potential_leak_all_list log_file_type $log_file_type_list {

        set slot_info [get_slot_info $log_file_path]
        set slot_info_in_command [::eagle_function::GetSlotInfoInCommand $slot_info]

        if {$log_file_type == $::eagle_analyze::USER_TYPE} {
            # 每个slot只获取一次用户态进程信息
            if {![info exists proJidList0($slot_info)]} {
                set proInfoList0 [ ::eagle_function::getAllUserPro $slot_info ]
                set proJidList0($slot_info) [ lindex $proInfoList0 0 ]
                set proNameList0($slot_info) [ lindex $proInfoList0 1 ]
            }
        }

        # 只有找到job才进行后面的操作
        set findjob false

        if {$log_file_type == $::eagle_analyze::USER_TYPE} {
            foreach jid $proJidList0($slot_info) jname $proNameList0($slot_info) {
                if {$mem_name == $jname} {
                    lappend job_id_list $jid
                    lappend job_name_list $mem_name
                    lappend job_type_list $::eagle_analyze::USER_TYPE
                    set findjob true
                    break
                }
            }

        } elseif {$log_file_type == $::eagle_analyze::TAG_TYPE} {
            lappend job_id_list $mem_name
            lappend job_name_list $mem_name
            lappend job_type_list $::eagle_analyze::TAG_TYPE
            set findjob true
        }

        if {true == $findjob} {
            lappend slot_info_in_command_list $slot_info_in_command
            lappend slot_info_list $slot_info
            lappend log_file_list $log_file_path
        }
    }

    #创建 Size 块记录文件
    array unset arr_new_log_file_id
    array unset arr_new_trace_log_file_id
    foreach log_file_path $log_file_list job_id $job_id_list ele $job_name_list slot_info $slot_info_list \
        slot_info_in_command $slot_info_in_command_list job_type $job_type_list {

        #创建Size记录文件
        set file_name_no_txt [string range $log_file_path 0 end-4]
        set new_log_file_path ${file_name_no_txt}-${ele}.txt
        set new_log_file_id [open $new_log_file_path w]
        set arr_new_log_file_id($job_id,$slot_info) $new_log_file_id

        if {$job_type == $::eagle_analyze::USER_TYPE} {
            # 对支持memory trace的设备，启动memory trace
            set cmdReturn [::eagle_function::MemoryTraceStart $job_id $slot_info_in_command]
            set new_trace_log_file_path ""
            set new_trace_log_file_id ""

            if {!($cmdReturn == $COMMOND_NOT_SUPPORT_VTP || [regexp -nocase "$COMMOND_NOT_SUPPORT_TCLSH" $cmdReturn] || $cmdReturn == $PROCESS_NOT_EXISTS)} {
                set new_trace_log_file_path ${file_name_no_txt}-trace-${ele}.log
                set new_trace_log_file_id [open $new_trace_log_file_path w]
                puts $new_trace_log_file_id "下发命令\nmemory trace job $job_id start $slot_info_in_command"
                puts $new_trace_log_file_id "返回信息\n$cmdReturn\n"
                puts $new_trace_log_file_id "下发 $::eagle_function::DETAIL_CHECK_COUNT 次拷机命令\n$cmd_list\n"
            }

            set arr_new_trace_log_file_id($job_id,$slot_info) $new_trace_log_file_id
        }
    }

    #下发10次命令，获取所有详细字节数据
    set comware_version [::eagle_function::getComwareVersion]
    array unset arr_result_list
    array unset arr_size_list_all
    for {set x 0} {$x < $::eagle_function::DETAIL_CHECK_COUNT} {incr x} {
        ::eagle_function::CommandProc $cmd_list $sysname

        foreach job_id $job_id_list slot_info $slot_info_list job_type $job_type_list {
            if {$job_type == $::eagle_analyze::USER_TYPE} {
                set result [::eagle_function::GetProcessHeapJobMemVerbose $job_id $slot_info]
            } elseif {$job_type == $::eagle_analyze::TAG_TYPE} {
                set result [::eagle_function::GetPoolTagMemVerbose $comware_version $job_id $slot_info]
            }

            set sizelist [lindex $result 0]
            lappend arr_result_list($job_id,$slot_info) $result
            append arr_size_list_all($job_id,$slot_info) " $sizelist"
        }
    }

    # 将数据写入记录文件
    foreach job_id $job_id_list slot_info $slot_info_list slot_info_in_command $slot_info_in_command_list job_type $job_type_list {
        set result_list $arr_result_list($job_id,$slot_info)
        set size_list_all $arr_size_list_all($job_id,$slot_info)

        set new_log_file_id $arr_new_log_file_id($job_id,$slot_info)

        #获取完整的Size列表，写入文件，避免有时候有空的情况
        if {$job_type == $::eagle_analyze::USER_TYPE} {
            set size_list_all [lsort -increasing [strlist_to_set $size_list_all]]
        } elseif {$job_type == $::eagle_analyze::TAG_TYPE} {
            set size_list_all [lsort -increasing [strlist_to_set $size_list_all]]
        }
        set line ""
        foreach sizeb $size_list_all {
            append line [format %20s $sizeb]
        }
        puts $new_log_file_id $line

        #获取完整的Size used列表，写入文件，Size为空时，写入0
        foreach result $result_list {
            set sizelist [lindex $result 0]
            set usedlist [lindex $result 1]
            set line ""
            foreach sizeb $size_list_all {
                set find 0
                foreach sizea $sizelist useda $usedlist {
                    if {$sizea == $sizeb} {
                        append line [format %20d $useda]
                        set find 1
                        continue
                    }
                }
                if {!$find} { append line [format %20d 0] }
            }
            puts $new_log_file_id $line
        }

        #关闭Size记录文件
        close $new_log_file_id

        if {$job_type == $::eagle_analyze::USER_TYPE} {
            # 对支持memory trace的设备，获取memory trace
            set new_trace_log_file_id $arr_new_trace_log_file_id($job_id,$slot_info)
            if {$new_trace_log_file_id != ""} {
                ::eagle_function::GetMemoryTraceJob $job_id $slot_info_in_command $new_trace_log_file_id
                ::eagle_function::MemoryTraceStop $job_id $slot_info_in_command $new_trace_log_file_id
                close $new_trace_log_file_id
            }
        }
    }
}

proc ::eagle_analyze::analyze_res_file_potential {log_file_path} {
    catch {
        ::log4tcl::step " 清空上一个文件数据!"
        init_eagle_analyze

        ::log4tcl::step " 读取日志文件!"
        read_log_file $log_file_path

        ::log4tcl::step " 获取没有变化的资源列表!"
        filter_no_change_mem

        ::log4tcl::step " 获取没有变化的资源数组，供Excel表写入用!"
        analysis_potential_resource_leak
    } errormsg
}

#!!================================================================
#过 程 名：  analysis_potential_resource_leak
#功能描述：  计算待分析资源泄露数组
#返 回 值： 无
#!!================================================================
proc ::eagle_analyze::analysis_potential_resource_leak {} {

    variable array_col_change
    variable mem_name_change_list
    variable array_col_need_analyze
    variable mem_name_need_analyze_list

    ::log4tcl::debug mem_name_change_list:$mem_name_change_list
    for {set col 0} {$col < [llength $mem_name_change_list]} {incr col} {
        set mem_name [lindex $mem_name_change_list $col]
        set mem_col_change_list $array_col_change($mem_name)
        set array_col_need_analyze($mem_name) $mem_col_change_list
        # lappend mem_name_need_analyze_list [string range $mem_diff [expr [string first @ $mem_diff]+1] end]
    }
    set mem_name_need_analyze_list $mem_name_change_list
    ::log4tcl::debug "待分析资源列表                : $mem_name_need_analyze_list"
}

proc ::eagle_analyze::print_res_change_info { terminal_name all_res_change_list init_log_dir excel_auto_open current_count_out} {
    set slot_info_list ""
    upvar $current_count_out current_count_in

    foreach {filename res_name} $all_res_change_list {
        lappend slot_info_list [get_excel_slot_info $filename]
    }
    set slot_info_list [lsort [strlist_to_set $slot_info_list]]

    set total_count 0
    foreach slot_info $slot_info_list {
        foreach {filename res_name} $all_res_change_list {
            # 多级目录处理
            set log_dir [file dir $init_log_dir/$filename]
            set file_pre_dir ""
            regexp {/([^/]+)$} $log_dir match file_pre_dir
            if {$file_pre_dir!= ""} {append file_pre_dir -}
            set filename [file tail $init_log_dir/$filename]

            set slot_info_in [get_excel_slot_info $filename]
            if {$slot_info_in == $slot_info} {
                set pre_info "$terminal_name"
                if {$slot_info != ""} {
                    set pre_info "$terminal_name-$slot_info"
                }
                set file_name_no_txt [string range $filename 0 end-5]
                incr current_count_in
                if {$current_count_in != 1} {
                    ::log4tcl::info ""
                }
                ::log4tcl::info "    $current_count_in、$pre_info ($res_name)"
                if {$excel_auto_open} {
                    ::log4tcl::info "           内存变化曲线见已打开Excel文件 ：${file_pre_dir}$filename，点击资源分析按钮"
                } else {
                    ::log4tcl::info "           内存变化曲线见                ：$log_dir/${file_pre_dir}$filename"
                }
            }
        }
    }
}

proc ::eagle_analyze::analyze_resource_file { log_file_path {need_excel_list 0} {init_log_dir "" }  {all_change_list_out ""}} {
    variable mem_name_change_list
    catch {
        analyze_res_file_potential $log_file_path

        if {$need_excel_list && $mem_name_change_list != ""} {
            upvar $all_change_list_out all_change_list_in
            set file_name $log_file_path
            regsub "$init_log_dir/" $file_name "" file_name
            set file_name_no_txt [string range $file_name 0 end-4]
            set excel_file_name $file_name_no_txt.xlsm
            lappend all_change_list_in "$excel_file_name"
            lappend all_change_list_in "$mem_name_change_list"
        }
    } errormsg
}

proc ::eagle_analyze::AnalyzeResourceChange {terminal_name init_log_path excel_auto_open write_not_potential} {
    namespace import ::eagle_excel::*
    #遍历指定目录，获取日志文件列表
    get_excel_col_list
    set ::eagle_analyze::log_file_list ""
    get_log_file_list "$init_log_path" res

    set log_count [llength $::eagle_analyze::log_file_list]
    set all_potential_num 0
    set all_not_change_log_list {}
    set all_change_list {}
    ::log4tcl::info "\n开始分析资源记录文件，并生成有可能有资源变化的Excel文件... "
    #遍历日志文件，生成分析结果
    for {set i 0} {$i < $log_count} {incr i} {

        set log_file_path [lindex $::eagle_analyze::log_file_list $i]
        ::log4tcl::setstepindex 1

        # 分析日志文件
        analyze_resource_file $log_file_path 1 $init_log_path all_change_list
        # 有内存泄露时，写Excel文件
        if {$::eagle_analyze::mem_name_change_list != ""} {
            incr all_potential_num [llength $::eagle_analyze::mem_name_change_list ]
            ::log4tcl::info "    [expr $i+1]、$log_file_path 有资源变化，开始生成Excel文件"
            set create_result [create_resource_file $log_file_path $excel_auto_open]
            if {$create_result == 0} {
                ::log4tcl::error "$log_file_path 生成Excel失败"
            }
        } else {
            ::log4tcl::info "    [expr $i+1]、$log_file_path 无资源变化"
            lappend all_not_change_log_list $log_file_path
        }
    }

    if {$all_potential_num == 0} {
        ::log4tcl::info "\n资源记录文件总体分析结论: 未发现资源变化模块。"
    } else {
        ::log4tcl::info "\n资源记录文件总体分析结论: 有 $all_potential_num 个模块可能存在资源变化，请分析确认... "
    }

    set current_count 0
    if {$all_change_list != ""} {
        print_res_change_info $terminal_name $all_change_list $init_log_path $excel_auto_open current_count
    }

    if {$write_not_potential} {
        ::log4tcl::info "\n开始生成无资源变化日志的excel数据，如果不需要可以修改config.tcl中参数write_not_potential。"
        for {set i 0} {$i < $log_count} {incr i} {
            set log_file_path [lindex $::eagle_analyze::log_file_list $i]
            ::log4tcl::setstepindex 1
            if {[lsearch $all_not_change_log_list $log_file_path] >= 0} {
                analyze_resource_file $log_file_path
                create_resource_file $log_file_path
            }
        }
    }
    return $all_potential_num
}

proc ::eagle_analyze::get_lipc_detail_info {slot} {
    set link_info  [::eagle_function::GetLipcPcbMbufStatistics]
    set recvbuf [lindex $link_info 1]
    set STCPRecvTotal [lindex $recvbuf 0]
    set STCPRecvMax [lindex $recvbuf 1]
    if {$STCPRecvTotal==0 && $STCPRecvMax ==0} {
        ::log4tcl::info "      未发现模块缓存信大量消息导致Lipc内存增长"
    } else {
        for {set i 0} {$i < 5} {incr i}  {
            set link_info  [::eagle_function::GetLipcPcbMbufStatistics]
        }
        set recvbuf [lindex $link_info 1]
        set STCP_Recv_Total [lindex $recvbuf 0]
        set STCP_Recv_Max [lindex $recvbuf 1]
        set STCP_Recv_Link [lindex $recvbuf 2]
        set STCP_Recv_Link_Port [lindex $recvbuf 4]
        if {$STCP_Recv_Total <$STCPRecvTotal ||  $STCP_Recv_Max <$STCPRecvMax} {
            ::log4tcl::info "      应用模块处理的不及时导致Lipc模块缓存了消息"
        } else {
            ::log4tcl::info "      LIPC缓存区出现持续增长消息，开始分析lipc可能挂死的模块"
            set last_lipc_stcp_link_recvcc ""
            set lipc_stcp_link_module ""
            set lipc_stcp_link_thread ""
            set lipc_stcp_link_recvcc ""

            set recvcc_not_change 1
            for {set i 0}  {$i < 5} {incr i} {
                set lipc_stcp_link [::eagle_function::GetLipcStcpLinkAll $STCP_Recv_Link_Port $STCP_Recv_Link]
                set lipc_stcp_link_module [lindex $lipc_stcp_link 0]
                set lipc_stcp_link_recvcc [lindex $lipc_stcp_link 2]
                if {$lipc_stcp_link_recvcc != $last_lipc_stcp_link_recvcc && $last_lipc_stcp_link_recvcc !=""} {
                    set recvcc_not_change 0
                    break
                }
                set last_lipc_stcp_link_recvcc $lipc_stcp_link_recvcc
            }
            if {$recvcc_not_change} {
                ::log4tcl::info "      模块 $lipc_stcp_link_module 线程 $lipc_stcp_link_thread  recvcc列一直未变化，开始检查模块栈信息"
                set stack_change [::eagle_function::GetThreadStack  $lipc_stcp_link_module $lipc_stcp_link_thread $slot]
                if {$stack_change} {
                    ::log4tcl::info "      模块 $lipc_stcp_link_module 线程 $lipc_stcp_link_thread  未挂死"
                } else {
                    ::log4tcl::info "      模块 $lipc_stcp_link_module 线程 $lipc_stcp_link_thread  已挂死！"
                }
            } else {
                ::log4tcl::info "      模块 $lipc_stcp_link_module 线程 $lipc_stcp_link_thread  recvcc列发生了变化，模块未挂死，请分析其他原因"

            }
        }
    }
}