# 部署说明

## 本地开发环境运行

```bash
python app.py
```

## 生产环境部署

### 选项1：使用Gunicorn（推荐）

1. 安装Gunicorn：
```bash
pip install gunicorn
```

2. 运行应用：
```bash
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
```

### 选项2：使用Heroku

1. 创建Procfile文件：
```
web: gunicorn wsgi:app
```

2. 部署到Heroku：
```bash
heroku create
git push heroku master
```

### 选项3：使用PythonAnywhere

1. 上传代码到PythonAnywhere
2. 配置WSGI应用指向wsgi.py
3. 设置静态文件路径

## 环境变量配置

生产环境建议设置以下环境变量：
- FLASK_ENV=production
- PORT=5000（或平台指定的端口）