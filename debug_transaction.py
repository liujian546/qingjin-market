import sqlite3

# 连接到数据库
conn = sqlite3.connect('marketplace.db')
cursor = conn.cursor()

# 检查transaction表结构
print("=== Transaction表结构 ===")
cursor.execute("PRAGMA table_info('transaction')")
columns = cursor.fetchall()
for column in columns:
    print(f"字段名: {column[1]}, 类型: {column[2]}, 是否可为空: {column[3]}, 默认值: {column[4]}")

print("\n=== Transaction表数据 ===")
cursor.execute("SELECT * FROM 'transaction' LIMIT 5")
transactions = cursor.fetchall()
for transaction in transactions:
    print(transaction)

print("\n=== Product表数据 ===")
cursor.execute("SELECT id, name, quantity, remaining_quantity FROM product LIMIT 5")
products = cursor.fetchall()
for product in products:
    print(product)

# 关闭连接
conn.close()