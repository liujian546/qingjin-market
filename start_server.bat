@echo off
echo ========================================
echo 校园交易平台服务器启动中...
echo ========================================
echo 本地访问: http://localhost:5000
echo 局域网访问: http://192.168.43.6:5000
echo.
echo 请确保防火墙允许5000端口的入站连接
echo 要从外部网络访问，请配置路由器端口转发
echo.
cd /d "c:\Users\Admin\my_first\campus_marketplace"
python run.py
pause