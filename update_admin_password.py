import sqlite3

# 连接到数据库
conn = sqlite3.connect('marketplace.db')
cursor = conn.cursor()

# 更新管理员密码
admin_student_id = '20250001'
new_password = 'ma7158192019'

try:
    cursor.execute('UPDATE user SET password = ? WHERE student_id = ?', (new_password, admin_student_id))
    
    if cursor.rowcount > 0:
        print(f"管理员账户 {admin_student_id} 的密码已成功更新为: {new_password}")
    else:
        print(f"未找到学号为 {admin_student_id} 的管理员账户")
        
    # 提交更改
    conn.commit()
    
except Exception as e:
    print(f"更新密码时出错: {e}")
    conn.rollback()
finally:
    conn.close()