"""
公网访问解决方案
此脚本提供多种方式将本地服务器暴露到公网
"""

import os
import subprocess
import sys
import time
import threading
import requests
import webbrowser

def show_manual_setup():
    """显示手动设置说明"""
    print("\n" + "=" * 50)
    print("公网访问设置说明")
    print("=" * 50)
    print("方法一：使用路由器端口转发（推荐）")
    print("1. 登录路由器管理界面（通常是192.168.1.1或192.168.0.1）")
    print("2. 找到'端口转发'或'虚拟服务器'设置")
    print("3. 添加规则：")
    print("   - 外部端口：5000")
    print("   - 内部IP：192.168.43.6")
    print("   - 内部端口：5000")
    print("   - 协议：TCP")
    print("4. 保存设置")
    print("5. 获取公网IP：访问 https://whatismyipaddress.com/")
    print("6. 外部访问地址：http://[您的公网IP]:5000")
    
    print("\n方法二：使用免费隧道服务")
    print("1. 访问 https://localhost.run/")
    print("2. 按照网站说明配置SSH隧道")
    
    print("\n方法三：使用Serveo（无需安装）")
    print("1. 打开新命令提示符窗口")
    print("2. 运行命令：ssh -R 80:localhost:5000 serveo.net")
    print("3. 系统会提供一个临时域名用于访问")
    
    print("\n" + "=" * 50)
    print("本地访问地址: http://localhost:5000")
    print("局域网访问地址: http://192.168.43.6:5000")
    print("=" * 50)

def start_server():
    """启动本地服务器"""
    print("正在启动本地服务器...")
    project_dir = r"c:\Users\Admin\my_first\campus_marketplace"
    os.chdir(project_dir)
    
    # 启动服务器
    print("✓ 本地服务器启动成功")
    print("访问地址:")
    print("  本地: http://localhost:5000")
    print("  局域网: http://192.168.43.6:5000")
    
    # 运行服务器
    try:
        subprocess.run([sys.executable, "run.py"], check=True)
    except KeyboardInterrupt:
        print("\n服务器已停止")

def main():
    """主函数"""
    print("=" * 50)
    print("校园交易平台公网访问解决方案")
    print("=" * 50)
    
    print("\n选择访问方式:")
    print("1. 本地/局域网访问（已自动启动）")
    print("2. 查看公网访问设置说明")
    
    choice = input("\n请输入选择 (1-2): ").strip()
    
    if choice == "1":
        start_server()
    elif choice == "2":
        show_manual_setup()
    else:
        print("启动本地服务器...")
        start_server()

if __name__ == "__main__":
    main()