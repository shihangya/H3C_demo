import re

def parse_cli_output(raw):
    """
    解析原始 CLI 输出，返回结构化数据字典：
        {
            'ar5drv 1': {'Tx': xxx, 'Rx': xxx},
            ...
        }
    """
    result = {}
    pattern = r"dis (ar5drv \d+) statistics.*?(TxFrameAllBytes|RxFrameAllBytes)\s+:\s+(\d+)"
    matches = re.findall(pattern, raw, re.DOTALL)

    for intf, direction, value in matches:
        value = int(value)
        if intf not in result:
            result[intf] = {}
        result[intf]['Tx' if 'Tx' in direction else 'Rx'] = value

    return result



def calculate_deltas(before, after):
    """
    计算每个接口的 Tx 和 Rx 字节增量
    """
    delta = {}

    for intf in before:
        if intf in after:
            tx_diff = after[intf].get('Tx', 0) - before[intf].get('Tx', 0)
            rx_diff = after[intf].get('Rx', 0) - before[intf].get('Rx', 0)
            delta[intf] = {'Tx': tx_diff, 'Rx': rx_diff}

    return delta


def print_delta_table(delta):
    """
    打印表格格式的结果
    """
    print(f"{'接口':<8} | {'Tx 发送增量 (bytes)':>18} | {'Rx 接收增量 (bytes)':>18}")
    print("-" * 50)

    for intf, values in sorted(delta.items()):
        print(f"{intf:<10} | {values['Tx']:>18} | {values['Rx']:>18}")


def main():
    # print("请输入【打流前】的 CLI 输出（粘贴完后按 Ctrl+D 结束输入）：")
    before_input = """
 
 
 [ap1-probe]dis ar5drv 1 statistics  | inc TxFrameAllBytes
 TxFrameAllBytes     : 145691726
[ap1-probe]dis ar5drv 1 statistics  | inc RxFrameAllBytes
 RxFrameAllBytes     : 880560312
[ap1-probe]dis ar5drv 2 statistics  | inc TxFrameAllBytes
 TxFrameAllBytes     : 138352686926
[ap1-probe]dis ar5drv 2 statistics  | inc RxFrameAllBytes
 RxFrameAllBytes     : 8749892118
[ap1-probe]dis ar5drv 3 statistics  | inc TxFrameAllBytes
 TxFrameAllBytes     : 195187102
[ap1-probe]dis ar5drv 3 statistics  | inc RxFrameAllBytes
 RxFrameAllBytes     : 7870403
 
 
 
 """

    #
    # print("\n请输入【打流后】的 CLI 输出（粘贴完后按 Ctrl+D 结束输入）：")
    after_input =  """
    
 [ap1-probe]dis ar5drv 1 statistics  | inc TxFrameAllBytes
 TxFrameAllBytes     : 146089438
[ap1-probe]dis ar5drv 1 statistics  | inc RxFrameAllBytes
 RxFrameAllBytes     : 906710144
[ap1-probe]dis ar5drv 2 statistics  | inc TxFrameAllBytes
 TxFrameAllBytes     : 139878849087
[ap1-probe]dis ar5drv 2 statistics  | inc RxFrameAllBytes
 RxFrameAllBytes     : 10509848382
[ap1-probe]dis ar5drv 3 statistics  | inc TxFrameAllBytes
 TxFrameAllBytes     : 196453720
[ap1-probe]dis ar5drv 3 statistics  | inc RxFrameAllBytes
 RxFrameAllBytes     : 7899706
 
 
 
 """

    before_data = parse_cli_output(before_input)
    after_data = parse_cli_output(after_input)

    print("Before Data:", before_data)
    print("After Data:", after_data)

    deltas = calculate_deltas(before_data, after_data)

    print("\n📊 流量变化统计结果：")
    print_delta_table(deltas)


if __name__ == "__main__":

    main()