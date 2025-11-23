# 支付配置文件

# 微信支付配置
WECHAT_APP_ID = 'your_wechat_app_id'
WECHAT_MCH_ID = 'your_wechat_mch_id'
WECHAT_API_KEY = 'your_wechat_api_key'
WECHAT_NOTIFY_URL = 'https://yourdomain.com/payment/wechat/notify'

# 支付宝配置
ALIPAY_APP_ID = 'your_alipay_app_id'
ALIPAY_PRIVATE_KEY = '''-----BEGIN RSA PRIVATE KEY-----
your_alipay_private_key
-----END RSA PRIVATE KEY-----'''
ALIPAY_PUBLIC_KEY = '''-----BEGIN PUBLIC KEY-----
your_alipay_public_key
-----END PUBLIC KEY-----'''
ALIPAY_NOTIFY_URL = 'https://yourdomain.com/payment/alipay/notify'

# 通用配置
PAYMENT_TIMEOUT = 3600  # 支付超时时间（秒）
REFUND_TIMEOUT = 86400  # 退款处理时间（秒）