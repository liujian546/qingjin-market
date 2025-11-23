"""
推送代码到GitHub的自动化脚本
"""

import os
import subprocess
import sys

def check_git():
    """检查Git是否已安装"""
    try:
        subprocess.run(["git", "--version"], check=True, capture_output=True)
        print("✓ Git已安装")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("✗ 未找到Git，请先安装Git")
        print("下载地址: https://git-scm.com/downloads")
        return False

def init_repo():
    """初始化Git仓库"""
    try:
        subprocess.run(["git", "init"], check=True, capture_output=True)
        print("✓ Git仓库初始化成功")
        return True
    except subprocess.CalledProcessError:
        print("✗ Git仓库初始化失败")
        return False

def add_files():
    """添加所有文件"""
    try:
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        print("✓ 文件添加成功")
        return True
    except subprocess.CalledProcessError:
        print("✗ 文件添加失败")
        return False

def create_commit():
    """创建提交"""
    try:
        subprocess.run(["git", "commit", "-m", "Initial commit of 青衿集校园交易平台"], 
                      check=True, capture_output=True)
        print("✓ 提交创建成功")
        return True
    except subprocess.CalledProcessError:
        print("✗ 提交创建失败")
        return False

def set_main_branch():
    """设置主分支"""
    try:
        subprocess.run(["git", "branch", "-M", "main"], check=True, capture_output=True)
        print("✓ 主分支设置成功")
        return True
    except subprocess.CalledProcessError:
        print("✗ 主分支设置失败")
        return False

def main():
    """主函数"""
    print("=" * 50)
    print("推送代码到GitHub自动化工具")
    print("=" * 50)
    
    # 切换到项目目录
    project_dir = r"c:\Users\Admin\my_first\campus_marketplace"
    os.chdir(project_dir)
    print(f"当前目录: {os.getcwd()}")
    
    # 检查Git
    if not check_git():
        return
    
    # 初始化仓库
    if not init_repo():
        return
    
    # 添加文件
    if not add_files():
        return
    
    # 创建提交
    if not create_commit():
        return
    
    # 设置主分支
    if not set_main_branch():
        return
    
    print("\n" + "=" * 50)
    print("下一步操作:")
    print("=" * 50)
    print("1. 在GitHub上创建仓库:")
    print("   - 访问 https://github.com/new")
    print("   - 仓库名称: qingjin-market")
    print("   - 选择Public")
    print("   - 不要初始化README")
    print("   - 点击'Create repository'")
    print()
    print("2. 连接远程仓库:")
    print("   git remote add origin https://github.com/你的用户名/qingjin-market.git")
    print()
    print("3. 推送代码:")
    print("   git push -u origin main")
    print("=" * 50)

if __name__ == "__main__":
    main()