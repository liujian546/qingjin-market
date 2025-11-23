import sqlite3

# 连接到数据库
conn = sqlite3.connect('marketplace.db')
cursor = conn.cursor()

# 检查transaction表是否缺少字段
cursor.execute('PRAGMA table_info("transaction")')
columns = [column[1] for column in cursor.fetchall()]

print("当前transaction表字段:", columns)

# 如果缺少amount字段，则添加
if 'amount' not in columns:
    print("添加amount字段...")
    cursor.execute('ALTER TABLE "transaction" ADD COLUMN amount FLOAT')

# 如果缺少fee字段，则添加
if 'fee' not in columns:
    print("添加fee字段...")
    cursor.execute('ALTER TABLE "transaction" ADD COLUMN fee FLOAT DEFAULT 0.1')

# 提交更改并关闭连接
conn.commit()
conn.close()

print("\n数据库结构已更新！")