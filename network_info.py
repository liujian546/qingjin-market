import socket
import subprocess
import re

def get_network_info():
    """获取详细的网络信息"""
    info = {}
    
    # 获取主机名
    info['hostname'] = socket.gethostname()
    
    # 获取所有网络接口IP
    try:
        # 使用ipconfig命令获取网络信息（Windows）
        result = subprocess.run(['ipconfig'], capture_output=True, text=True, shell=True)
        output = result.stdout
        
        # 提取IPv4地址
        ipv4_pattern = r'IPv4 Address[.\s]*:\s*(\d+\.\d+\.\d+\.\d+)'
        ipv4_matches = re.findall(ipv4_pattern, output)
        info['ipv4_addresses'] = ipv4_matches
    except Exception as e:
        info['error'] = str(e)
        info['ipv4_addresses'] = []
    
    return info

def get_local_ip():
    """获取本机在局域网中的IP地址"""
    try:
        # 创建一个UDP socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 连接到一个远程地址（这里使用Google的DNS）
        s.connect(("8.8.8.8", 80))
        # 获取本地IP地址
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        # 如果无法获取，则返回默认值
        return "127.0.0.1"

if __name__ == "__main__":
    print("=== 网络信息 ===")
    network_info = get_network_info()
    print(f"主机名: {network_info['hostname']}")
    
    if 'ipv4_addresses' in network_info:
        print("IPv4地址:")
        for ip in network_info['ipv4_addresses']:
            print(f"  - {ip}")
    
    print("\n=== 局域网访问地址 ===")
    local_ip = get_local_ip()
    print(f"http://{local_ip}:5000")
    
    print("\n=== 访问说明 ===")
    print("1. 同一局域网内的设备可以通过上述地址访问")
    print("2. 要从外部网络访问，需要配置路由器端口转发")
    print("3. 端口转发设置：将外部端口5000转发到本机IP的5000端口")