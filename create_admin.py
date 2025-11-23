import sqlite3

# 连接到数据库
conn = sqlite3.connect('marketplace.db')
cursor = conn.cursor()

# 删除可能存在的错误管理员账户
cursor.execute("DELETE FROM user WHERE student_id='20250001' AND username!='admin'")

# 确保有一个正确的管理员账户
cursor.execute("""
    INSERT OR REPLACE INTO user (id, student_id, phone, username, email, password, is_admin) 
    VALUES (1, '20250001', '13800138001', 'admin', 'admin@example.com', 'admin123', 1)
""")

# 提交更改并关闭连接
conn.commit()
conn.close()

print("管理员账户已创建/更新！")
print("管理员账户信息：")
print("学号：20250001")
print("用户名：admin")
print("密码：admin123")