@echo off
echo ========================================
echo 青衿集校园交易平台 - Heroku完整部署脚本
echo ========================================
echo.

echo 步骤1: 登录Heroku
echo 请在打开的浏览器中完成登录...
echo.
D:\heroku\bin\heroku.cmd login
if %errorlevel% neq 0 (
    echo Heroku登录失败
    pause
    exit /b
)
echo ✓ Heroku登录成功
echo.

echo 步骤2: 创建Heroku应用
echo 正在创建应用...
D:\heroku\bin\heroku.cmd create qingjin-market-liujian546
if %errorlevel% neq 0 (
    echo 应用创建失败，尝试使用自动生成的名称...
    D:\heroku\bin\heroku.cmd create
    if %errorlevel% neq 0 (
        echo 应用创建失败
        pause
        exit /b
    )
)
echo ✓ 应用创建成功
echo.

echo 步骤3: 设置环境变量
D:\heroku\bin\heroku.cmd config:set FLASK_APP=app.py
if %errorlevel% neq 0 (
    echo 环境变量设置失败
    pause
    exit /b
)
D:\heroku\bin\heroku.cmd config:set FLASK_ENV=production
if %errorlevel% neq 0 (
    echo 环境变量设置失败
    pause
    exit /b
)
echo ✓ 环境变量设置成功
echo.

echo 步骤4: 推送代码到Heroku
echo 正在推送代码，请稍候...
git push heroku main
if %errorlevel% neq 0 (
    echo 代码推送失败
    pause
    exit /b
)
echo ✓ 代码推送成功
echo.

echo 步骤5: 打开应用
D:\heroku\bin\heroku.cmd open
echo.

echo ========================================
echo 部署完成！
echo ========================================
echo 您的青衿集校园交易平台已成功部署到Heroku
echo 后续更新只需运行: git push heroku main
echo.
pause