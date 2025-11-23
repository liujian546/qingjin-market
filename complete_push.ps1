# 完整推送脚本
Write-Host "设置工作目录..."
Set-Location "c:\Users\Admin\my_first\campus_marketplace"

Write-Host "检查Git状态..."
git status

Write-Host "添加所有文件..."
git add .

Write-Host "提交更改..."
git commit -m "Final commit for GitHub push"

Write-Host "推送代码到GitHub..."
git push -u origin main

Write-Host "推送完成!"