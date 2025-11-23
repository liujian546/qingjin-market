@echo off
echo ========================================
echo 青衿集校园交易平台 - GitHub推送工具
echo GitHub用户名: liujian546
echo ========================================
echo.

echo 正在推送代码到GitHub...
echo 仓库地址: https://github.com/liujian546/qingjin-market.git
echo.

echo 步骤1: 设置远程仓库
git remote add origin https://github.com/liujian546/qingjin-market.git
if %errorlevel% neq 0 (
    echo 可能已设置过远程仓库，继续下一步...
    echo.
)

echo 步骤2: 推送代码到GitHub
echo 首次推送可能需要较长时间，请耐心等待...
git push -u origin main
if %errorlevel% neq 0 (
    echo 推送失败，请检查网络连接或GitHub仓库设置
    pause
    exit /b
)

echo.
echo ========================================
echo 推送完成！
echo ========================================
echo 您的代码已成功推送到GitHub
echo 访问 https://github.com/liujian546/qingjin-market 查看仓库
echo.
echo 后续更新只需运行: git push
echo.
pause