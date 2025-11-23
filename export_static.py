"""
导出静态网站版本用于GitHub Pages部署
"""

import os
import shutil
import sys
from app import app

def export_static_site():
    """导出静态网站"""
    print("正在导出静态网站...")
    
    # 创建输出目录
    output_dir = "static_site"
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    
    # 复制静态文件
    if os.path.exists("static"):
        shutil.copytree("static", os.path.join(output_dir, "static"))
    
    # 复制模板文件并转换为静态页面
    if os.path.exists("templates"):
        shutil.copytree("templates", os.path.join(output_dir, "templates"))
    
    # 创建index.html
    index_content = """
<!DOCTYPE html>
<html>
<head>
    <title>青衿集 - 校园二手交易平台</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container">
        <div class="row">
            <div class="col-12 text-center mt-5">
                <h1>青衿集 - 校园二手交易平台</h1>
                <p class="lead">这是一个基于GitHub Pages的静态演示版本</p>
                <div class="alert alert-info mt-4">
                    <h4>功能说明</h4>
                    <ul class="text-start">
                        <li>商品浏览和搜索</li>
                        <li>商品分类展示</li>
                        <li>响应式设计，支持移动端</li>
                    </ul>
                </div>
                <div class="alert alert-warning mt-4">
                    <h4>注意</h4>
                    <p>此静态版本仅用于演示界面，实际功能需要部署到服务器环境</p>
                    <p>完整功能版本可通过以下方式访问：</p>
                    <ul class="text-start">
                        <li>使用SSH隧道：ssh -R 80:localhost:5000 nokey@localhost.run</li>
                        <li>部署到Heroku等云平台</li>
                        <li>使用GitHub Codespaces</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
    """
    
    with open(os.path.join(output_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_content)
    
    print(f"静态网站已导出到: {output_dir}")
    print("您可以将此目录内容推送到GitHub仓库并启用GitHub Pages")

if __name__ == "__main__":
    export_static_site()