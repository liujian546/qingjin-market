@echo off
echo ========================================
echo 校园交易平台公网访问启动工具
echo ========================================
echo.

echo 正在启动本地服务器...
cd /d "c:\Users\Admin\my_first\campus_marketplace"
start "" python run.py

timeout /t 3 /nobreak >nul

echo.
echo 本地服务器已启动:
echo   本地访问: http://localhost:5000
echo   局域网访问: http://192.168.43.6:5000
echo.

echo 创建公网访问隧道...
echo 请在新窗口中查看公网访问地址
echo.
echo 如果这是您第一次使用此服务，可能会提示确认SSH连接
echo 请选择"是"或"yes"继续
echo.
pause

ssh -R 80:localhost:5000 localhost.run

echo.
echo 按任意键退出...
pause