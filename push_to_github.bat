@echo off
echo ========================================
echo 推送代码到GitHub
echo ========================================

echo 正在初始化Git仓库...
cd /d "c:\Users\Admin\my_first\campus_marketplace"
git init

echo 正在添加所有文件...
git add .

echo 正在创建提交...
git commit -m "Initial commit of 青衿集校园交易平台"

echo 正在设置主分支...
git branch -M main

echo 请在GitHub上创建名为 qingjin-market 的仓库
echo 然后按任意键继续...
pause

echo 请替换下面的 yourusername 为您的GitHub用户名
echo 运行以下命令连接到远程仓库:
echo git remote add origin https://github.com/yourusername/qingjin-market.git
echo.

echo 推送代码到GitHub:
echo git push -u origin main
echo.

echo 按任意键退出...
pause