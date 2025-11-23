import sqlite3
import os

# 连接到数据库
db_path = 'marketplace.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 备份现有用户数据（如果存在）
users_backup = []
try:
    cursor.execute("SELECT username, email, password, is_blacklisted, created_at FROM user")
    users_backup = cursor.fetchall()
    print(f"备份了 {len(users_backup)} 个用户")
except sqlite3.OperationalError:
    print("没有找到现有用户表")

# 删除旧的用户表
try:
    cursor.execute("DROP TABLE user")
    print("删除了旧的用户表")
except sqlite3.OperationalError:
    print("没有找到用户表需要删除")

# 创建新的用户表
cursor.execute("""
    CREATE TABLE user (
        id INTEGER PRIMARY KEY,
        student_id VARCHAR(20) UNIQUE,
        phone VARCHAR(11) UNIQUE,
        username VARCHAR(80) NOT NULL,
        email VARCHAR(120) UNIQUE NOT NULL,
        password VARCHAR(120) NOT NULL,
        is_blacklisted BOOLEAN DEFAULT 0,
        is_admin BOOLEAN DEFAULT 0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
""")

print("创建了新的用户表")

# 恢复用户数据（如果存在）
if users_backup:
    for user in users_backup:
        cursor.execute("""
            INSERT INTO user (username, email, password, is_blacklisted, created_at) 
            VALUES (?, ?, ?, ?, ?)
        """, user)
    print(f"恢复了 {len(users_backup)} 个用户")

# 创建管理员账户
cursor.execute("""
    INSERT OR IGNORE INTO user (student_id, phone, username, email, password, is_admin) 
    VALUES (?, ?, ?, ?, ?, ?)
""", ('20250001', '13800138001', 'admin', 'admin@example.com', 'admin123', 1))

print("创建了管理员账户")

# 提交更改并关闭连接
conn.commit()
conn.close()

print("\n管理员账户初始化完成！")
print("管理员账户信息：")
print("学号：20250001")
print("密码：admin123")