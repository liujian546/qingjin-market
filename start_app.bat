@echo off
echo 青衿集启动脚本
echo ======================

REM 检查是否已安装Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误：未找到Python，请先安装Python
    pause
    exit /b
)

REM 激活虚拟环境（如果存在）
if exist "venv\Scripts\activate.bat" (
    echo 正在激活虚拟环境...
    call venv\Scripts\activate.bat
)

REM 安装依赖（如果requirements.txt存在）
if exist "requirements.txt" (
    echo 正在安装依赖...
    pip install -r requirements.txt >nul 2>&1
)

REM 设置Flask环境变量
set FLASK_APP=app.py
set FLASK_ENV=development

REM 启动应用
echo 正在启动青衿集...
echo 请在浏览器中访问以下地址：
echo 本地访问: http://127.0.0.1:5000
echo 网络访问: http://你的电脑IP地址:5000
echo 按 Ctrl+C 停止服务
python app.py

pause