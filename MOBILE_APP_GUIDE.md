# 校园交易平台移动应用配置

## 应用信息
- 应用名称: 校园交易平台
- 版本: 1.0.0
- 描述: 校园线上交易平台，支持商品发布、交易和信用管理

## 技术栈
- 前端框架: Flask + Bootstrap
- 后端框架: Flask
- 数据库: SQLite
- 打包工具: Cordova/PhoneGap 或 PWA

## 打包说明

### 方法一：PWA (推荐)
1. 确保 manifest.json 文件配置正确
2. 添加 Service Worker 支持离线功能
3. 使用 HTTPS 部署应用
4. 通过浏览器添加到主屏幕功能安装

### 方法二：Cordova/PhoneGap
1. 安装 Cordova: `npm install -g cordova`
2. 创建 Cordova 项目: `cordova create campus-marketplace`
3. 添加平台: `cordova platform add android ios`
4. 复制 Web 应用文件到 www 目录
5. 构建应用: `cordova build`

### 方法三：Flutter (需要重构)
1. 使用 Flutter 重新构建 UI
2. 保留 Flask 后端 API
3. 构建跨平台移动应用

## 应用商店发布
- 遵循各应用商店的发布指南
- 确保符合校园相关政策
- 提供清晰的用户隐私政策