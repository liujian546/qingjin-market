"""
快速启动脚本
此脚本可以一键启动校园交易平台服务器
"""

import os
import subprocess
import sys
import webbrowser
import time

def main():
    """主函数"""
    print("=" * 50)
    print("校园交易平台快速启动工具")
    print("=" * 50)
    
    # 切换到项目目录
    project_dir = r"c:\Users\Admin\my_first\campus_marketplace"
    os.chdir(project_dir)
    
    print("正在启动服务器...")
    print("本地访问地址: http://localhost:5000")
    print("局域网访问地址: http://192.168.43.6:5000")
    print("\n提示:")
    print("1. 请确保Windows防火墙允许5000端口的入站连接")
    print("2. 要从外部网络访问，请配置路由器端口转发")
    print("3. 按Ctrl+C停止服务器")
    print("-" * 50)
    
    try:
        # 启动服务器
        subprocess.run([sys.executable, "run.py"], check=True)
    except KeyboardInterrupt:
        print("\n服务器已停止")
    except Exception as e:
        print(f"启动失败: {e}")

if __name__ == "__main__":
    main()