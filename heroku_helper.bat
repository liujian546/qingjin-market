@echo off
echo Heroku Helper Script
echo ===================

if "%1"=="" (
    echo 用法: heroku_helper.bat [command]
    echo 示例: heroku_helper.bat login
    echo 示例: heroku_helper.bat apps
    echo 示例: heroku_helper.bat create
    exit /b
)

echo 执行命令: D:\heroku\bin\heroku.cmd %*
D:\heroku\bin\heroku.cmd %*