"""
Heroku + GitHub 自动化部署脚本
"""

import os
import subprocess
import sys
import webbrowser

def check_heroku_cli():
    """检查Heroku CLI是否已安装"""
    try:
        result = subprocess.run(["heroku", "--version"], check=True, capture_output=True)
        print("✓ Heroku CLI已安装")
        print(result.stdout.decode('utf-8'))
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("✗ 未找到Heroku CLI，请先安装:")
        print("  访问: https://devcenter.heroku.com/articles/heroku-cli")
        return False

def login_heroku():
    """登录Heroku"""
    try:
        print("正在打开浏览器进行Heroku登录...")
        subprocess.run(["heroku", "login"], check=True)
        print("✓ Heroku登录成功")
        return True
    except subprocess.CalledProcessError:
        print("✗ Heroku登录失败")
        return False

def create_heroku_app():
    """创建Heroku应用"""
    app_name = input("请输入Heroku应用名称（留空则自动生成）: ").strip()
    
    try:
        if app_name:
            result = subprocess.run(["heroku", "create", app_name], check=True, capture_output=True)
        else:
            result = subprocess.run(["heroku", "create"], check=True, capture_output=True)
        
        output = result.stdout.decode('utf-8')
        print("✓ Heroku应用创建成功")
        print(output)
        
        # 提取应用URL
        lines = output.split('\n')
        for line in lines:
            if 'https://' in line and '.herokuapp.com' in line:
                app_url = line.strip()
                print(f"应用URL: {app_url}")
                return app_url
        return None
    except subprocess.CalledProcessError as e:
        print("✗ Heroku应用创建失败")
        print(e.stderr.decode('utf-8'))
        return None

def set_config_vars():
    """设置环境变量"""
    try:
        subprocess.run(["heroku", "config:set", "FLASK_APP=app.py"], check=True)
        subprocess.run(["heroku", "config:set", "FLASK_ENV=production"], check=True)
        print("✓ 环境变量设置成功")
        return True
    except subprocess.CalledProcessError:
        print("✗ 环境变量设置失败")
        return False

def setup_github_integration():
    """设置GitHub集成说明"""
    print("\n" + "=" * 50)
    print("GitHub集成设置说明")
    print("=" * 50)
    print("1. 访问Heroku控制台: https://dashboard.heroku.com/")
    print("2. 选择您的应用")
    print("3. 点击'Deploy'选项卡")
    print("4. 在'Deployment method'部分选择'GitHub'")
    print("5. 搜索并连接到您的'qingjin-market'仓库")
    print("6. 启用'Automatic deploys'")
    print("7. 点击'Deploy Branch'部署main分支")
    print("=" * 50)

def main():
    """主函数"""
    print("=" * 50)
    print("青衿集校园交易平台 - Heroku自动化部署")
    print("=" * 50)
    
    # 切换到项目目录
    project_dir = r"c:\Users\Admin\my_first\campus_marketplace"
    os.chdir(project_dir)
    print(f"当前目录: {os.getcwd()}")
    
    # 检查Heroku CLI
    if not check_heroku_cli():
        return
    
    # 登录Heroku
    if not login_heroku():
        return
    
    # 创建Heroku应用
    app_url = create_heroku_app()
    if not app_url:
        return
    
    # 设置环境变量
    if not set_config_vars():
        return
    
    # 设置GitHub集成
    setup_github_integration()
    
    print("\n" + "=" * 50)
    print("部署完成!")
    print("=" * 50)
    print(f"您的应用已部署到: {app_url}")
    print("后续推送代码到GitHub将自动触发部署")
    print("访问应用URL即可查看青衿集校园交易平台")
    print("=" * 50)
    
    # 打开应用URL
    try:
        webbrowser.open(app_url)
        print("已打开浏览器访问您的应用")
    except:
        pass

if __name__ == "__main__":
    main()