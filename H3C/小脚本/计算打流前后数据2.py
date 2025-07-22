import re

def parse_scb_data(text):
    # 提取 MAC 地址和 AID
    mac_match = re.search(r"SCB MAC Address:\s*([\d:a-fA-F]+).*?AID:\s*(\d+)", text)
    if not mac_match:
        raise ValueError("未找到 MAC 地址或 AID，请检查输入格式")

    mac_address = mac_match.group(1)
    aid = int(mac_match.group(2))

    result = {
        "mac": mac_address,
        "aid": aid,
        "links": {}
    }

    # 按照 link 分割数据块
    blocks = re.split(r"link:\s*(\d+)", text)[1:]  # [index, content, index, content...]

    for i in range(0, len(blocks), 2):
        link_id = int(blocks[i])
        block_content = blocks[i + 1]

        # 提取每个字段（使用默认值 0 防止匹配失败）
        try:
            tx = int(re.search(r"scb tx packets:\s*(\d+)", block_content).group(1))
        except:
            tx = 0

        try:
            tx_failed = int(re.search(r"scb tx failed packets:\s*(\d+)", block_content).group(1))
        except:
            tx_failed = 0

        try:
            tx_total = int(re.search(r"scb tx total packets:\s*(\d+)", block_content).group(1))
        except:
            tx_total = 0

        try:
            rx = int(re.search(r"scb rx packets:\s*(\d+)", block_content).group(1))
        except:
            rx = 0

        result["links"][link_id] = {
            "tx": tx,
            "tx_failed": tx_failed,
            "tx_total": tx_total,
            "rx": rx
        }

    return result


def calculate_deltas(before_data, after_data):
    deltas = {
        "mac": after_data["mac"],
        "aid": after_data["aid"],
        "links": {}
    }

    for link_id, before_stats in before_data["links"].items():
        if link_id in after_data["links"]:
            after_stats = after_data["links"][link_id]
            deltas["links"][link_id] = {
                "tx": after_stats["tx"] - before_stats["tx"],
                "tx_failed": after_stats["tx_failed"] - before_stats["tx_failed"],
                "tx_total": after_stats["tx_total"] - before_stats["tx_total"],
                "rx": after_stats["rx"] - before_stats["rx"],
            }

    return deltas


def print_delta_table(delta_data):
    print(f"\n📊 SCB MAC: {delta_data['mac']} | AID: {delta_data['aid']}")
    print(f"{'Link':<6} | {'Tx packets增量':>10} | {'Tx Failed增量':>12} | {'Tx Total增量':>10} | {'Rx packets增量':>10}")
    print("-" * 70)

    for link_id, stats in sorted(delta_data["links"].items()):
        print(
            f"{link_id:<6} | "
            f"{stats['tx']:>15} | "
            f"{stats['tx_failed']:>10} | "
            f"{stats['tx_total']:>15} | "
            f"{stats['rx']:>10}"
        )


# ========== 主函数示例 ==========
if __name__ == "__main__":
    before_text = """
    
SCB MAC Address: 76:3D:65:D2:E8:4E AID: 552
link: 0-----------------------------------
scb tx packets: 306078
scb tx failed packets: 0
scb tx total packets: 320935
scb rx packets: 46388
scb rssi window: -22 rssi chain window -- chain1: -22 chain 2: -38 chain 3: -21 chain 4: -24
scb rssi window: -22 rssi chain window -- chain1: -22 chain 2: -38 chain 3: -21 chain 4: -24
scb rssi window: -22 rssi chain window -- chain1: -22 chain 2: -38 chain 3: -21 chain 4: -24
scb rssi window: -22 rssi chain window -- chain1: -22 chain 2: -38 chain 3: -21 chain 4: -24
link: 1-----------------------------------
scb tx packets: 0
scb tx failed packets: 0
scb tx total packets: 0
scb rx packets: 0
link: 2-----------------------------------
scb tx packets: 9265
scb tx failed packets: 0
scb tx total packets: 17614
scb rx packets: 10289
scb rssi window: -3 rssi chain window -- chain1: -3 chain 2: -14 chain 3: -2 chain 4: -16
scb rssi window: -2 rssi chain window -- chain1: -17 chain 2: -10 chain 3: -1 chain 4: -9
scb rssi window: -4 rssi chain window -- chain1: -3 chain 2: -13 chain 3: -21 chain 4: -12
scb rssi window: -3 rssi chain window -- chain1: -3 chain 2: -17 chain 3: -2 chain 4: -16
link: 3-----------------------------------
scb tx packets: 0
scb tx failed packets: 0
scb tx total packets: 0
scb rx packets: 0

    """

    after_text = """
    
SCB MAC Address: 76:3D:65:D2:E8:4E AID: 552
link: 0-----------------------------------
scb tx packets: 613029
scb tx failed packets: 0
scb tx total packets: 642308
scb rx packets: 88145
scb rssi window: -16 rssi chain window -- chain1: -17 chain 2: -33 chain 3: -16 chain 4: -20
scb rssi window: -16 rssi chain window -- chain1: -17 chain 2: -33 chain 3: -16 chain 4: -20
scb rssi window: -16 rssi chain window -- chain1: -17 chain 2: -33 chain 3: -16 chain 4: -20
scb rssi window: -16 rssi chain window -- chain1: -17 chain 2: -33 chain 3: -16 chain 4: -21
link: 1-----------------------------------
scb tx packets: 0
scb tx failed packets: 0
scb tx total packets: 0
scb rx packets: 0
link: 2-----------------------------------
scb tx packets: 12084
scb tx failed packets: 0
scb tx total packets: 22939
scb rx packets: 16217
scb rssi window: -1 rssi chain window -- chain1: -17 chain 2: -10 chain 3: -1 chain 4: -9
scb rssi window: -9 rssi chain window -- chain1: -15 chain 2: -10 chain 3: -4 chain 4: -9
scb rssi window: -1 rssi chain window -- chain1: -2 chain 2: -10 chain 3: -1 chain 4: -9
scb rssi window: -1 rssi chain window -- chain1: -15 chain 2: -10 chain 3: -1 chain 4: -9
link: 3-----------------------------------
scb tx packets: 0
scb tx failed packets: 0
scb tx total packets: 0
scb rx packets: 0


    """

    before_data = parse_scb_data(before_text)
    after_data = parse_scb_data(after_text)
    print("Before Data:", before_data)
    print("After Data:", after_data)

    delta = calculate_deltas(before_data, after_data)

    print_delta_table(delta)