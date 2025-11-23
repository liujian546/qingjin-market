import sqlite3

# 连接到数据库
conn = sqlite3.connect('marketplace.db')
cursor = conn.cursor()

# 检查sold_at字段是否存在
cursor.execute("PRAGMA table_info(product)")
columns = [column[1] for column in cursor.fetchall()]

print("当前product表字段:", columns)

# 如果缺少sold_at字段，则添加
if 'sold_at' not in columns:
    print("添加sold_at字段...")
    cursor.execute('ALTER TABLE product ADD COLUMN sold_at DATETIME')

# 提交更改并关闭连接
conn.commit()
conn.close()

print("\n数据库结构已更新！")