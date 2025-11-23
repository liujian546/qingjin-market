import sqlite3

# 连接到数据库
conn = sqlite3.connect('marketplace.db')
cursor = conn.cursor()

# 检查表结构
cursor.execute("PRAGMA table_info(user)")
columns = [column[1] for column in cursor.fetchall()]

print("当前user表字段:", columns)

# 检查是否有phone字段，如果有则删除（因为我们不再使用）
# SQLite不支持直接删除列，所以我们需要创建新表

# 检查是否有is_blacklisted字段
if 'is_blacklisted' not in columns:
    print("添加is_blacklisted字段...")
    cursor.execute('ALTER TABLE user ADD COLUMN is_blacklisted BOOLEAN DEFAULT 0')

# 提交更改并关闭连接
conn.commit()
conn.close()

print("\n数据库结构已更新！")