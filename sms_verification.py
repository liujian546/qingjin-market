import random
import time

# 模拟短信验证码存储（实际应用中应使用Redis等）
verification_codes = {}

def send_verification_code(phone):
    """
    模拟发送短信验证码
    实际应用中应集成短信服务API
    """
    # 生成6位随机验证码
    code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    
    # 保存验证码和时间戳（5分钟有效期）
    verification_codes[phone] = {
        'code': code,
        'timestamp': time.time()
    }
    
    # 实际应用中这里会调用短信服务API发送验证码
    print(f"发送验证码 {code} 到手机号 {phone}")
    
    return code

def verify_code(phone, code):
    """
    验证短信验证码
    """
    if phone not in verification_codes:
        return False
    
    stored_data = verification_codes[phone]
    
    # 检查验证码是否过期（5分钟）
    if time.time() - stored_data['timestamp'] > 300:
        del verification_codes[phone]
        return False
    
    # 验证验证码
    if stored_data['code'] == code:
        # 验证成功后删除验证码
        del verification_codes[phone]
        return True
    
    return False

# 测试函数
if __name__ == "__main__":
    # 测试发送验证码
    test_phone = "13800138000"
    send_verification_code(test_phone)
    
    # 测试验证验证码
    # print(verify_code(test_phone, "123456"))  # 应该返回False