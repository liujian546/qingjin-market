# 测试Heroku安装脚本
Write-Host "测试Heroku CLI安装..."
Write-Host "========================"

# 尝试多种方式运行Heroku
$herokuPaths = @(
    "heroku",
    "C:\Program Files\heroku\bin\heroku.cmd",
    "C:\Program Files (x86)\Heroku\bin\heroku.cmd",
    "$env:LOCALAPPDATA\heroku\bin\heroku.cmd"
)

foreach ($path in $herokuPaths) {
    try {
        Write-Host "尝试: $path"
        $result = & $path --version 2>$null
        if ($result) {
            Write-Host "成功! Heroku版本: $result"
            exit 0
        }
    } catch {
        Write-Host "失败: $path"
    }
}

Write-Host "未能找到有效的Heroku安装"
Write-Host "请重新安装Heroku CLI并确保添加到系统PATH"