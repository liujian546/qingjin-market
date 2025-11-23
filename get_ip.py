import socket

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
    local_ip = get_local_ip()
    print(f"本机局域网IP地址: {local_ip}")
    print(f"局域网访问地址: http://{local_ip}:5000")