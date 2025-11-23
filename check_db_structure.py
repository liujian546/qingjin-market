import sqlite3

# 连接到数据库
conn = sqlite3.connect('marketplace.db')
cursor = conn.cursor()

# 检查所有表结构
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("数据库中的所有表:")
for table in tables:
    print(f"- {table[0]}")

# 检查用户表结构
print("\n用户表结构:")
cursor.execute("PRAGMA table_info(user);")
user_columns = cursor.fetchall()
for column in user_columns:
    print(f"- {column[1]} ({column[2]})")

# 检查商品分类表结构
print("\n商品分类表结构:")
try:
    cursor.execute("PRAGMA table_info(category);")
    category_columns = cursor.fetchall()
    for column in category_columns:
        print(f"- {column[1]} ({column[2]})")
except:
    print("category表不存在")

# 检查商品表结构
print("\n商品表结构:")
try:
    cursor.execute("PRAGMA table_info(product);")
    product_columns = cursor.fetchall()
    for column in product_columns:
        print(f"- {column[1]} ({column[2]})")
except:
    print("product表不存在")

conn.close()