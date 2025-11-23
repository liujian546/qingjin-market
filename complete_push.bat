@echo off
echo ========================================
echo 青衿集校园交易平台 - GitHub推送工具
echo ========================================
echo.

echo 步骤1: 在GitHub上创建仓库
echo 请访问 https://github.com/new
echo 创建一个名为 qingjin-market 的仓库
echo 确保选择 Public 并且不要初始化 README
echo.
pause

echo 步骤2: 设置远程仓库
echo 请将 your-github-username 替换为您的GitHub用户名
echo 然后运行以下命令:
echo.
echo git remote add origin https://github.com/your-github-username/qingjin-market.git
echo.
pause

echo 步骤3: 推送代码到GitHub
echo 运行以下命令推送代码:
echo.
echo git push -u origin main
echo.
pause

echo 推送完成!
echo 您的代码现在已推送到GitHub
echo 访问 https://github.com/your-github-username/qingjin-market 查看仓库
echo.
echo 后续推送只需运行: git push
echo.
pause