"""
WSGI config for campus marketplace project.
This module contains the WSGI application used by any WSGI server.
"""

import os
import sys

# 添加项目路径到Python路径
sys.path.insert(0, os.path.dirname(__file__))

from app import app

if __name__ == "__main__":
    app.run()