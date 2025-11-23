import sqlite3

# 连接到数据库
conn = sqlite3.connect('marketplace.db')
cursor = conn.cursor()

# 查询所有用户
cursor.execute('SELECT id, student_id, phone, username, email, password, is_admin FROM user')
users = cursor.fetchall()

print('当前用户列表:')
for user in users:
    print(f"ID: {user[0]}, 学号: {user[1]}, 手机: {user[2]}, 用户名: {user[3]}, 邮箱: {user[4]}, 密码: {user[5]}, 管理员: {user[6]}")

conn.close()