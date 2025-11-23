import time
from functools import wraps
from flask import request, session, jsonify
import hashlib

class RateLimiter:
    def __init__(self):
        # 存储每个IP的请求记录 {ip: [timestamp1, timestamp2, ...]}
        self.requests = {}
        # 时间窗口（秒）
        self.window = 60
        # 最大请求数
        self.max_requests = 100
    
    def is_allowed(self, ip):
        """检查是否允许该IP的请求"""
        now = time.time()
        
        # 初始化该IP的请求记录
        if ip not in self.requests:
            self.requests[ip] = []
        
        # 清除窗口外的旧请求记录
        self.requests[ip] = [req_time for req_time in self.requests[ip] if now - req_time < self.window]
        
        # 检查是否超过限制
        if len(self.requests[ip]) >= self.max_requests:
            return False
        
        # 记录当前请求
        self.requests[ip].append(now)
        return True
    
    def get_remaining_requests(self, ip):
        """获取剩余请求数"""
        if ip not in self.requests:
            return self.max_requests
        now = time.time()
        self.requests[ip] = [req_time for req_time in self.requests[ip] if now - req_time < self.window]
        return max(0, self.max_requests - len(self.requests[ip]))

# 创建全局速率限制器实例
rate_limiter = RateLimiter()

def rate_limit(max_requests=100, window=60):
    """速率限制装饰器"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # 获取客户端IP
            ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
            
            # 更新速率限制器配置
            rate_limiter.max_requests = max_requests
            rate_limiter.window = window
            
            # 检查是否超过速率限制
            if not rate_limiter.is_allowed(ip):
                return jsonify({
                    'error': '请求过于频繁，请稍后再试',
                    'retry_after': rate_limiter.window
                }), 429
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def get_client_ip():
    """获取客户端真实IP"""
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        return request.environ['REMOTE_ADDR']
    else:
        return request.environ['HTTP_X_FORWARDED_FOR']

def generate_csrf_token():
    """生成CSRF令牌"""
    if 'csrf_token' not in session:
        session['csrf_token'] = hashlib.sha256(str(time.time()).encode()).hexdigest()
    return session['csrf_token']

def validate_csrf_token(token):
    """验证CSRF令牌"""
    return 'csrf_token' in session and session['csrf_token'] == token

def sanitize_input(text):
    """简单的输入清理函数"""
    if not text:
        return text
    # 移除潜在的危险字符
    dangerous_chars = ['<', '>', '&', '"', "'", ';', '--', '/*', '*/']
    for char in dangerous_chars:
        text = text.replace(char, '')
    return text.strip()

def validate_student_id(student_id):
    """验证学号格式"""
    if not student_id:
        return False
    # 学号应该是数字，长度在6-20之间
    return student_id.isdigit() and 6 <= len(student_id) <= 20

def validate_email(email):
    """简单验证邮箱格式"""
    if not email:
        return False
    return '@' in email and '.' in email and len(email) > 5

def validate_password(password):
    """验证密码强度"""
    if not password:
        return False
    # 密码长度至少6位
    return len(password) >= 6