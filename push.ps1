# PowerShell推送脚本
Write-Host "开始推送代码到GitHub..."
Set-Location "c:\Users\Admin\my_first\campus_marketplace"
git push -u origin main
Write-Host "推送完成!"