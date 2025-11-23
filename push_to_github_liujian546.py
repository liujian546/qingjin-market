"""
推送代码到liujian546的GitHub仓库
"""

import os
import subprocess
import sys

def run_command(command):
    """运行命令并返回结果"""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"错误: {e}")
        print(f"stderr: {e.stderr}")
        return False

def main():
    """主函数"""
    print("=" * 50)
    print("青衿集校园交易平台 - GitHub推送工具")
    print("GitHub用户名: liujian546")
    print("=" * 50)
    
    # 切换到项目目录
    project_dir = r"c:\Users\Admin\my_first\campus_marketplace"
    os.chdir(project_dir)
    print(f"当前目录: {os.getcwd()}")
    
    # 设置远程仓库
    print("\n步骤1: 设置远程仓库")
    remote_command = "git remote add origin https://github.com/liujian546/qingjin-market.git"
    if not run_command(remote_command):
        print("可能已设置过远程仓库，继续下一步...")
    
    # 推送代码
    print("\n步骤2: 推送代码到GitHub")
    print("首次推送可能需要较长时间，请耐心等待...")
    push_command = "git push -u origin main"
    if run_command(push_command):
        print("\n" + "=" * 50)
        print("推送完成！")
        print("=" * 50)
        print("您的代码已成功推送到GitHub")
        print("访问 https://github.com/liujian546/qingjin-market 查看仓库")
        print("\n后续更新只需运行: git push")
        print("=" * 50)
    else:
        print("\n推送失败，请检查网络连接或GitHub仓库设置")

if __name__ == "__main__":
    main()