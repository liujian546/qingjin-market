"""
Production run script for campus marketplace.
Supports both Windows and Unix-like systems.
"""

import os
import sys

# 添加项目路径到Python路径
sys.path.insert(0, os.path.dirname(__file__))

from app import app

if __name__ == "__main__":
    # 生产环境配置
    app.config['DEBUG'] = False
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    
    # 启动应用
    app.run(
        host=host,
        port=port
    )