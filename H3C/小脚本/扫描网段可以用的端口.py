import requests
import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib3
from typing import List, Tuple

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def check_http_endpoint(ip: str, port: int = 8080, path: str = "/imc", timeout: int = 5) -> Tuple[bool, str]:
    """
    检查指定IP的HTTP端点是否可访问

    Args:
        ip: 目标IP地址
        port: 端口号，默认8080
        path: 路径，默认/imc
        timeout: 超时时间，默认5秒

    Returns:
        tuple: (是否可访问, 状态码/错误信息)
    """
    urls = [
        f"http://{ip}:{port}{path}",
        f"https://{ip}:{port}{path}"
    ]

    for url in urls:
        try:
            response = requests.get(url, timeout=timeout, verify=False)
            if response.status_code == 200:
                return True, f"Status: {response.status_code}"
            elif response.status_code < 500:
                # 4xx错误表示服务存在但拒绝访问
                return True, f"Status: {response.status_code}"
        except requests.exceptions.SSLError:
            # SSL错误但仍可能服务存在
            if url.startswith("https"):
                continue
        except requests.exceptions.RequestException:
            # 网络错误或其他请求异常
            continue
        except Exception:
            continue

    return False, "Unreachable"

def generate_ip_range(start_ip: str, end_ip: str) -> List[str]:
    """
    生成IP范围列表

    Args:
        start_ip: 起始IP
        end_ip: 结束IP

    Returns:
        IP地址列表
    """
    start = ipaddress.IPv4Address(start_ip)
    end = ipaddress.IPv4Address(end_ip)

    # 确保起始IP小于结束IP
    if start > end:
        start, end = end, start

    # 生成所有IP地址
    ips = []
    current_ip = start
    while current_ip <= end:
        ips.append(str(current_ip))
        current_ip += 1

    return ips

def scan_imc_endpoints(start_ip: str = "8.1.1.1", end_ip: str = "8.1.1.255",
                      port: int = 8080, path: str = "/imc") -> None:
    """
    扫描IP范围内指定端点的可访问性

    Args:
        start_ip: 起始IP地址
        end_ip: 结束IP地址
        port: 端口号
        path: 路径
    """
    # 生成IP范围
    ips = generate_ip_range(start_ip, end_ip)

    accessible_hosts = []

    print(f"开始扫描 {start_ip} 到 {end_ip} 范围内端口 {port}{path} 的可访问性...")
    print("=" * 60)

    # 使用线程池并发检查
    with ThreadPoolExecutor(max_workers=50) as executor:
        # 提交所有检查任务
        future_to_ip = {
            executor.submit(check_http_endpoint, ip, port, path): ip
            for ip in ips
        }

        # 处理完成的任务
        for future in as_completed(future_to_ip):
            ip = future_to_ip[future]
            try:
                is_accessible, status = future.result()
                if is_accessible:
                    accessible_hosts.append((ip, status))
                    print(f"✓ 发现可访问主机: {ip}:{port}{path} ({status})")
            except Exception as e:
                print(f"✗ 检查 {ip} 时发生错误: {e}")

    # 输出最终结果
    print("\n" + "=" * 60)
    print("扫描完成！")
    print("=" * 60)

    if accessible_hosts:
        print("以下地址可以访问:")
        for ip, status in sorted(accessible_hosts, key=lambda x: ipaddress.IPv4Address(x[0])):
            print(f"  {ip}:{port}{path} ({status})")
    else:
        print("未发现可访问的地址")

if __name__ == "__main__":
    scan_imc_endpoints()
