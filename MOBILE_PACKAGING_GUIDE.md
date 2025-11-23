# 校园交易平台移动应用打包指南

## 概述
本文档介绍了如何将校园交易平台打包为移动端APP并上架到应用商店。

## 技术方案
我们采用混合应用开发方案，基于以下技术：
- 前端：HTML5 + CSS3 + JavaScript (Bootstrap 5)
- 后端：Flask (Python)
- 打包工具：Apache Cordova
- 数据库：SQLite

## 打包步骤

### 1. 环境准备
```bash
# 安装 Node.js (推荐 LTS 版本)
# 安装 Cordova CLI
npm install -g cordova

# 安装 Android Studio (用于 Android 打包)
# 安装 Xcode (用于 iOS 打包，仅限 macOS)
```

### 2. 创建 Cordova 项目
```bash
# 创建 Cordova 项目
cordova create campus-marketplace-app com.campus.marketplace.app "校园交易平台"

# 进入项目目录
cd campus-marketplace-app

# 添加平台支持
cordova platform add android
cordova platform add ios
```

### 3. 集成 Web 应用
```bash
# 删除默认的 www 目录内容
rm -rf www/*

# 将 Flask 应用的静态文件复制到 www 目录
cp -r /path/to/campus_marketplace/static/* www/
cp -r /path/to/campus_marketplace/templates/* www/

# 构建 Flask 应用的 API 接口（可选）
# 或者将 Flask 应用部署到服务器，移动端通过网络访问
```

### 4. 配置应用
```bash
# 复制配置文件
cp /path/to/campus_marketplace/config.xml ./

# 复制图标和启动页
cp -r /path/to/campus_marketplace/static/icons ./www/
cp -r /path/to/campus_marketplace/static/splash ./www/
```

### 5. 构建应用
```bash
# 构建 Android 应用
cordova build android

# 构建 iOS 应用 (仅限 macOS)
cordova build ios
```

### 6. 测试应用
```bash
# 在 Android 设备上测试
cordova run android

# 在 iOS 模拟器上测试 (仅限 macOS)
cordova run ios
```

## 应用商店上架指南

### Google Play Store (Android)
1. 创建 Google Play 开发者账户 ($25 一次性费用)
2. 准备应用截图和描述
3. 生成签名 APK 或 App Bundle
4. 填写应用信息并上传
5. 提交审核

### Apple App Store (iOS)
1. 加入 Apple Developer Program ($99/年)
2. 使用 Xcode 生成签名应用
3. 在 App Store Connect 创建应用
4. 填写应用信息和截图
5. 提交审核

## 注意事项
1. 确保遵守各应用商店的政策和指南
2. 应用图标和截图需要符合平台规范
3. 应用描述需要准确反映应用功能
4. 确保应用在各种设备上正常运行
5. 遵守数据隐私和安全相关法规

## 后续维护
1. 定期更新应用以修复 bug 和添加新功能
2. 监控应用评价和用户反馈
3. 根据用户需求优化用户体验
4. 保持与 Web 版本的功能同步