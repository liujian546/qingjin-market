import sqlite3

# 连接到数据库
conn = sqlite3.connect('marketplace.db')
cursor = conn.cursor()

# 检查transaction表结构
print("Transaction表结构:")
cursor.execute('PRAGMA table_info("transaction")')
columns = cursor.fetchall()
for column in columns:
    print(f"- {column[1]} ({column[2]})")

# 检查其他表结构
print("\nProduct表结构:")
cursor.execute('PRAGMA table_info(product)')
columns = cursor.fetchall()
for column in columns:
    print(f"- {column[1]} ({column[2]})")

print("\nUser表结构:")
cursor.execute('PRAGMA table_info(user)')
columns = cursor.fetchall()
for column in columns:
    print(f"- {column[1]} ({column[2]})")

conn.close()