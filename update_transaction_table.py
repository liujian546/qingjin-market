import sqlite3

# 连接到数据库
conn = sqlite3.connect('marketplace.db')
cursor = conn.cursor()

# 检查表结构
cursor.execute("PRAGMA table_info('transaction')")
columns = [column[1] for column in cursor.fetchall()]

print("当前transaction表字段:", columns)

# 检查是否有quantity字段
if 'quantity' not in columns:
    print("添加quantity字段...")
    cursor.execute("ALTER TABLE 'transaction' ADD COLUMN quantity INTEGER DEFAULT 1")

# 提交更改并关闭连接
conn.commit()
conn.close()

print("\n数据库结构已更新！")