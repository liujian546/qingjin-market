@echo off
echo ========================================
echo 青衿集校园交易平台 - Heroku部署向导
echo ========================================
echo.

echo 步骤1: 检查Heroku CLI
echo 确保已安装Heroku CLI
echo 下载地址: https://devcenter.heroku.com/articles/heroku-cli
echo.
pause

echo 步骤2: 登录Heroku
echo 将打开浏览器进行登录，请完成登录流程
echo.
heroku login
if %errorlevel% neq 0 (
    echo Heroku登录失败，请重试
    pause
    exit /b
)
echo ✓ Heroku登录成功
echo.

echo 步骤3: 创建Heroku应用
set /p appname=请输入应用名称（留空则自动生成）: 
if "%appname%"=="" (
    heroku create
) else (
    heroku create %appname%
)
if %errorlevel% neq 0 (
    echo Heroku应用创建失败，请重试
    pause
    exit /b
)
echo.

echo 步骤4: 设置环境变量
heroku config:set FLASK_APP=app.py
heroku config:set FLASK_ENV=production
echo ✓ 环境变量设置完成
echo.

echo 步骤5: 推送代码到Heroku
echo 正在推送代码，请稍候...
git push heroku main
if %errorlevel% neq 0 (
    echo 代码推送失败，请检查网络连接
    pause
    exit /b
)
echo.

echo 步骤6: 打开应用
echo 正在打开您的应用...
heroku open
echo.

echo ========================================
echo 部署完成！
echo ========================================
echo 您的青衿集校园交易平台已成功部署到Heroku
echo 后续更新只需运行: git push heroku main
echo.
pause