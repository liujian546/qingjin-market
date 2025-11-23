import sqlite3

# 连接到数据库
conn = sqlite3.connect('marketplace.db')
cursor = conn.cursor()

# 检查product表是否缺少字段
cursor.execute("PRAGMA table_info(product);")
columns = [column[1] for column in cursor.fetchall()]

print("当前product表字段:", columns)

# 如果缺少category_id字段，则添加
if 'category_id' not in columns:
    print("添加category_id字段...")
    cursor.execute("ALTER TABLE product ADD COLUMN category_id INTEGER")
    # 为现有商品设置默认分类ID为1（假设"其他"分类的ID为1）
    cursor.execute("UPDATE product SET category_id = 1 WHERE category_id IS NULL")

# 如果缺少image_url字段，则添加
if 'image_url' not in columns:
    print("添加image_url字段...")
    cursor.execute("ALTER TABLE product ADD COLUMN image_url VARCHAR(200)")

# 如果缺少外键约束，则添加
try:
    # 添加外键约束需要重新创建表，这里我们只添加必要的字段
    print("数据库表结构修复完成")
except Exception as e:
    print(f"添加约束时出错: {e}")

# 提交更改并关闭连接
conn.commit()
conn.close()

print("\n数据库结构已更新！")