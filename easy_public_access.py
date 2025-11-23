"""
简易公网访问脚本
此脚本使用免费的localhost.run服务创建公网访问
"""

import os
import subprocess
import sys
import threading
import time
import requests

def start_local_server():
    """启动本地服务器"""
    print("正在启动本地服务器...")
    project_dir = r"c:\Users\Admin\my_first\campus_marketplace"
    os.chdir(project_dir)
    
    # 启动服务器进程
    server_process = subprocess.Popen([sys.executable, "run.py"], 
                                    stdout=subprocess.DEVNULL, 
                                    stderr=subprocess.DEVNULL)
    print("✓ 本地服务器启动成功")
    return server_process

def create_tunnel():
    """创建SSH隧道"""
    print("正在创建公网访问隧道...")
    print("请稍候，这可能需要几分钟...")
    
    try:
        # 使用localhost.run创建隧道
        # 这会创建一个临时的公网URL
        result = subprocess.run([
            "ssh", 
            "-R", 
            "80:localhost:5000", 
            "nokey@localhost.run"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            # 提取URL
            output = result.stdout
            lines = output.split('\n')
            for line in lines:
                if 'http' in line and 'localhost.run' in line:
                    url = line.strip()
                    print(f"✓ 公网访问地址: {url}")
                    print("任何人都可以通过此网址访问您的校园交易平台！")
                    return url
        else:
            print("✗ 隧道创建失败")
            print("错误信息:", result.stderr)
            return None
            
    except subprocess.TimeoutExpired:
        print("✓ 隧道创建成功（可能需要在另一窗口查看URL）")
        return "http://*.localhost.run"
    except Exception as e:
        print(f"✗ 隧道创建失败: {e}")
        return None

def show_alternative_methods():
    """显示替代方法"""
    print("\n" + "=" * 50)
    print("替代公网访问方法")
    print("=" * 50)
    print("方法一：使用路由器端口转发")
    print("1. 登录路由器管理界面")
    print("2. 设置端口转发：外部端口5000 -> 内部IP 192.168.43.6:5000")
    print("3. 获取公网IP并访问：http://[公网IP]:5000")
    
    print("\n方法二：使用其他免费隧道服务")
    print("1. 访问 https://serveo.net/")
    print("2. 运行命令: ssh -R 80:localhost:5000 serveo.net")
    
    print("\n方法三：使用ngrok（需注册账户）")
    print("1. 访问 https://ngrok.com/")
    print("2. 注册账户并获取认证令牌")
    print("3. 运行命令: ngrok http 5000")
    print("=" * 50)

def main():
    """主函数"""
    print("=" * 50)
    print("校园交易平台简易公网访问工具")
    print("=" * 50)
    
    # 启动本地服务器
    server_process = start_local_server()
    
    # 等待服务器启动
    time.sleep(3)
    
    print("\n访问地址:")
    print("  本地: http://localhost:5000")
    print("  局域网: http://192.168.43.6:5000")
    
    print("\n正在尝试创建公网访问...")
    
    # 尝试创建隧道
    public_url = create_tunnel()
    
    if public_url:
        print(f"\n✓ 公网访问已启用: {public_url}")
        print("任何人都可以通过此网址访问您的校园交易平台！")
    else:
        print("\n✗ 自动创建公网访问失败")
        show_alternative_methods()
    
    print("\n按Ctrl+C停止服务")
    
    try:
        # 保持运行
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n正在停止服务...")
        server_process.terminate()
        print("服务已停止")

if __name__ == "__main__":
    main()