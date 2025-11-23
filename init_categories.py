import sqlite3

# 连接到数据库
conn = sqlite3.connect('marketplace.db')
cursor = conn.cursor()

# 检查是否已有分类数据
cursor.execute("SELECT COUNT(*) FROM category")
count = cursor.fetchone()[0]

if count == 0:
    # 创建默认分类
    categories = [
        ('书籍资料', '教材、参考书、笔记等'),
        ('电子产品', '手机、电脑、耳机等'),
        ('生活用品', '日用品、装饰品等'),
        ('服装鞋帽', '衣服、鞋子、配饰等'),
        ('运动健身', '运动器材、健身用品等'),
        ('其他', '其他各类商品')
    ]
    
    cursor.executemany("INSERT INTO category (name, description) VALUES (?, ?)", categories)
    print("已创建默认商品分类")
else:
    print("商品分类已存在")

# 提交更改并关闭连接
conn.commit()
conn.close()

print("分类数据初始化完成！")