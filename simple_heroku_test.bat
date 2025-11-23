@echo off
echo 测试Heroku CLI安装...
echo ========================

echo 尝试运行: heroku --version
heroku --version
if %errorlevel% equ 0 (
    echo Heroku CLI 已正确安装并配置
) else (
    echo Heroku CLI 未正确安装或未添加到PATH
    echo 请重新安装Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
)

pause