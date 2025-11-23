"""
一键部署脚本
此脚本可以帮助您将应用部署到常见的云平台
"""

import os
import subprocess
import sys

def check_prerequisites():
    """检查部署前提条件"""
    print("检查部署前提条件...")
    
    # 检查Python
    try:
        subprocess.run([sys.executable, "--version"], check=True, capture_output=True)
        print("✓ Python已安装")
    except subprocess.CalledProcessError:
        print("✗ 未找到Python，请先安装Python")
        return False
    
    return True

def install_dependencies():
    """安装依赖"""
    print("安装依赖包...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("✓ 依赖包安装成功")
        return True
    except subprocess.CalledProcessError:
        print("✗ 依赖包安装失败")
        return False

def deploy_to_heroku():
    """部署到Heroku"""
    print("部署到Heroku...")
    
    # 检查Heroku CLI
    try:
        subprocess.run(["heroku", "--version"], check=True, capture_output=True)
        print("✓ Heroku CLI已安装")
    except subprocess.CalledProcessError:
        print("✗ 未找到Heroku CLI，请先安装：https://devcenter.heroku.com/articles/heroku-cli")
        return False
    
    try:
        # 创建Heroku应用
        subprocess.run(["heroku", "create"], check=True)
        
        # 部署代码
        subprocess.run(["git", "push", "heroku", "master"], check=True)
        
        # 打开应用
        subprocess.run(["heroku", "open"], check=True)
        
        print("✓ 应用已成功部署到Heroku")
        return True
    except subprocess.CalledProcessError:
        print("✗ Heroku部署失败")
        return False

def deploy_to_pythonanywhere():
    """部署到PythonAnywhere说明"""
    print("\n部署到PythonAnywhere:")
    print("1. 访问 https://www.pythonanywhere.com/")
    print("2. 注册或登录账户")
    print("3. 进入'Files'标签页，上传所有项目文件")
    print("4. 进入'Web'标签页，创建新Web应用")
    print("5. 选择'Flask'框架和对应的Python版本")
    print("6. 配置WSGI文件指向wsgi.py")
    print("7. 设置静态文件路径：/static/ -> /home/用户名/项目名/static/")
    print("8. 重新加载应用")

def main():
    """主函数"""
    print("=" * 50)
    print("校园交易平台一键部署工具")
    print("=" * 50)
    
    if not check_prerequisites():
        return
    
    if not install_dependencies():
        return
    
    print("\n选择部署平台:")
    print("1. Heroku (需要先安装Heroku CLI)")
    print("2. PythonAnywhere")
    print("3. 其他平台 (手动部署)")
    
    choice = input("\n请输入选择 (1-3): ").strip()
    
    if choice == "1":
        deploy_to_heroku()
    elif choice == "2":
        deploy_to_pythonanywhere()
    elif choice == "3":
        print("\n手动部署说明:")
        print("1. 安装依赖: pip install -r requirements.txt")
        print("2. 使用Gunicorn运行: gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app")
        print("3. 或使用Python运行: python run.py")
        print("4. 配置反向代理(如Nginx)和域名解析")
    else:
        print("无效选择")

if __name__ == "__main__":
    main()