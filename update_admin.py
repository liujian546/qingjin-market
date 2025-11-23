import sqlite3

# 连接到数据库
db_path = 'marketplace.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 更新第一个用户为管理员
cursor.execute("UPDATE user SET student_id='20250001', phone='13800138001', is_admin=1 WHERE id=1")

# 提交更改并关闭连接
conn.commit()
conn.close()

print("管理员账户更新完成！")