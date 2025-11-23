from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
import time
import threading
import re
import subprocess
import socket
from datetime import datetime, timedelta
from PIL import Image
from security import rate_limiter, sanitize_input, validate_student_id, validate_email, validate_password

# Add this import to handle the url_quote issue
try:
    from werkzeug.urls import url_quote
except ImportError:
    from urllib.parse import quote as url_quote

app = Flask(__name__)
app.config['SECRET_KEY'] = 'campus_marketplace_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///marketplace.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(os.path.join(app.root_path, app.config['UPLOAD_FOLDER']), exist_ok=True)

db = SQLAlchemy(app)

# 数据模型定义
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), unique=True, nullable=False)  # 学号
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_blacklisted = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)  # 管理员标识
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Category {self.name}>'

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200))  # 商品图片路径
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)  # 商品分类
    status = db.Column(db.String(20), default='available')  # available, reserved, sold
    meeting_location = db.Column(db.String(200), nullable=True)
    meeting_time = db.Column(db.String(200), nullable=True)  # 交易时间
    contact_info = db.Column(db.String(100), nullable=True)  # 联系方式
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    sold_at = db.Column(db.DateTime, nullable=True)  # 售出时间
    quantity = db.Column(db.Integer, default=1)  # 商品数量
    remaining_quantity = db.Column(db.Integer, default=1)  # 剩余数量
    
    seller = db.relationship('User', foreign_keys=[seller_id])
    buyer = db.relationship('User', foreign_keys=[buyer_id])
    category = db.relationship('Category')  # 商品分类关系
    transactions = db.relationship('Transaction', back_populates='product', lazy=True)  # 与交易的关系
    
    def __repr__(self):
        return f'<Product {self.name}>'

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, completed, cancelled
    amount = db.Column(db.Float, nullable=False)  # 交易金额
    fee = db.Column(db.Float, default=0.1)  # 手续费
    quantity = db.Column(db.Integer, default=1)  # 交易数量
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    product = db.relationship('Product', back_populates='transactions')
    seller = db.relationship('User', foreign_keys=[seller_id])
    buyer = db.relationship('User', foreign_keys=[buyer_id])

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reporter_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reported_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, resolved
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    reporter = db.relationship('User', foreign_keys=[reporter_id])
    reported_user = db.relationship('User', foreign_keys=[reported_user_id])
    transaction = db.relationship('Transaction')

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', foreign_keys=[user_id])
    
    def __repr__(self):
        return f'<Notification {self.id}>'

# 创建数据库表
@app.before_first_request
def create_tables():
    db.create_all()
    
    # 创建默认分类
    if Category.query.count() == 0:
        categories = [
            Category(name='书籍资料', description='教材、参考书、笔记等'),
            Category(name='电子产品', description='手机、电脑、耳机等'),
            Category(name='生活用品', description='日用品、装饰品等'),
            Category(name='服装鞋帽', description='衣服、鞋子、配饰等'),
            Category(name='运动健身', description='运动器材、健身用品等'),
            Category(name='其他', description='其他各类商品')
        ]
        for category in categories:
            db.session.add(category)
        db.session.commit()

# 路由定义
@app.route('/')
def index():
    # 传递Notification模型到模板上下文
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    category_id = request.args.get('category', type=int)
    
    # 构建查询，只显示可购买和已预订的商品（不显示已下架和已售出的）
    query = Product.query.filter(Product.status.in_(['available', 'reserved']))
    
    # 应用搜索条件
    if search:
        query = query.filter(Product.name.contains(search))
    
    # 应用分类筛选
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    # 按创建时间倒序排列并分页
    products = query.order_by(Product.created_at.desc()).paginate(
        page=page, per_page=6, error_out=False)
    
    # 获取所有分类用于筛选
    categories = Category.query.all()
    
    return render_template('index.html', 
                         products=products.items,
                         pagination=products,
                         categories=categories,
                         selected_category=category_id,
                         search=search,
                         Notification=Notification)

@app.route('/register', methods=['GET', 'POST'])
def register():
    # 传递Notification模型到模板上下文
    if request.method == 'POST':
        student_id = sanitize_input(request.form['student_id'])
        username = sanitize_input(request.form['username'])
        email = sanitize_input(request.form['email'])
        password = request.form['password']
        
        # 输入验证
        if not validate_student_id(student_id):
            flash('学号格式不正确，应为6-20位数字')
            return render_template('register.html', Notification=Notification)
        
        if not validate_email(email):
            flash('邮箱格式不正确')
            return render_template('register.html', Notification=Notification)
        
        if not validate_password(password):
            flash('密码长度至少6位')
            return render_template('register.html', Notification=Notification)
        
        # 检查学号、邮箱或用户名是否已存在
        existing_user = User.query.filter((User.student_id == student_id) | 
                                         (User.email == email) |
                                         (User.username == username)).first()
        if existing_user:
            flash('学号、邮箱或用户名已存在')
            return render_template('register.html', Notification=Notification)
        
        # 创建新用户
        new_user = User(student_id=student_id, username=username, 
                       email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('注册成功，请登录')
        return redirect(url_for('login'))
    
    return render_template('register.html', Notification=Notification)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # 传递Notification模型到模板上下文
    if request.method == 'POST':
        student_id = sanitize_input(request.form['student_id'])
        password = request.form['password']
        
        # 输入验证
        if not validate_student_id(student_id):
            flash('学号格式不正确')
            return render_template('login.html', Notification=Notification)
        
        # 支持学号登录
        user = User.query.filter(
            User.student_id == student_id,
            User.password == password
        ).first()
        
        if user:
            # 检查用户是否被注销或封禁
            if user.is_blacklisted:
                flash('您的账户已被注销或封禁')
                return render_template('login.html', Notification=Notification)
            
            session['user_id'] = user.id
            session['username'] = user.username
            session['is_admin'] = user.is_admin  # 保存管理员状态
            
            # 如果是管理员，重定向到管理员面板
            if user.is_admin:
                return redirect(url_for('admin_panel'))
            
            return redirect(url_for('index'))
        else:
            flash('学号或密码错误')
    
    return render_template('login.html', Notification=Notification)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/products/new', methods=['GET', 'POST'])
def new_product():
    # 传递Notification模型到模板上下文
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = sanitize_input(request.form['name'])
        description = sanitize_input(request.form['description'])
        price = float(request.form['price'])
        quantity = int(request.form.get('quantity', 1))  # 获取数量，默认为1
        category_id = int(request.form['category_id'])
        meeting_location = sanitize_input(request.form.get('meeting_location', ''))
        meeting_time = sanitize_input(request.form.get('meeting_time', ''))  # 新增字段
        contact_info = sanitize_input(request.form.get('contact_info', ''))  # 新增字段
        
        # 输入验证
        if not name or len(name) < 1 or len(name) > 100:
            flash('商品名称长度应在1-100个字符之间')
            categories = Category.query.all()
            return render_template('new_product.html', categories=categories, Notification=Notification)
        
        if not description or len(description) < 1:
            flash('商品描述至少1个字符')
            categories = Category.query.all()
            return render_template('new_product.html', categories=categories, Notification=Notification)
        
        if price <= 0 or price > 10000:
            flash('商品价格应在0-10000之间')
            categories = Category.query.all()
            return render_template('new_product.html', categories=categories, Notification=Notification)
        
        if quantity < 1 or quantity > 100:
            flash('商品数量应在1-100之间')
            categories = Category.query.all()
            return render_template('new_product.html', categories=categories, Notification=Notification)
        
        if not meeting_time:
            flash('请输入交易时间')
            categories = Category.query.all()
            return render_template('new_product.html', categories=categories, Notification=Notification)
        
        # 处理图片上传
        image_url = None
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file and image_file.filename != '':
                # 生成唯一的文件名
                filename = f"product_{int(datetime.utcnow().timestamp())}_{secure_filename(image_file.filename)}"
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                
                # 优化并保存图片
                optimize_image(image_file, save_path)
                image_url = f"/static/uploads/{filename}"
        
        # 创建新商品
        new_product = Product(
            name=name,
            description=description,
            price=price,
            quantity=quantity,  # 设置总数量
            remaining_quantity=quantity,  # 设置剩余数量
            category_id=category_id,
            meeting_location=meeting_location,
            meeting_time=meeting_time,
            contact_info=contact_info,
            seller_id=session['user_id'],
            image_url=image_url
        )
        
        db.session.add(new_product)
        db.session.commit()
        
        flash('商品发布成功！')
        return redirect(url_for('index'))
    
    # GET请求时显示发布商品表单
    categories = Category.query.all()
    return render_template('new_product.html', categories=categories, Notification=Notification)

@app.route('/products/<int:product_id>')
def product_detail(product_id):
    # 传递Notification模型到模板上下文
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product, Notification=Notification)

@app.route('/products/<int:product_id>/buy', methods=['GET', 'POST'])
def buy_product(product_id):
    # 传递Notification模型到模板上下文
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    product = Product.query.get_or_404(product_id)
    
    # 检查商品是否可购买
    if product.status != 'available':
        flash('该商品不可购买')
        return redirect(url_for('product_detail', product_id=product_id))
    
    # 检查是否有剩余数量
    if product.remaining_quantity <= 0:
        flash('该商品已售罄')
        return redirect(url_for('product_detail', product_id=product_id))
    
    if request.method == 'POST':
        try:
            # 获取买方填写的信息
            quantity = int(request.form.get('quantity', 1))
            address = request.form.get('address', '')
            contact_info = request.form.get('contact_info', '')
            
            # 验证数量
            if quantity < 1 or quantity > product.remaining_quantity:
                flash(f'购买数量必须在1-{product.remaining_quantity}之间')
                return redirect(url_for('buy_product', product_id=product_id))
            
            # 计算总金额
            total_amount = product.price * quantity
            
            # 创建交易记录
            transaction = Transaction(
                product_id=product.id,
                seller_id=product.seller_id,
                buyer_id=session['user_id'],
                amount=total_amount,
                fee=calculate_fee(session['user_id']) * quantity,  # 按数量计算手续费
                quantity=quantity  # 保存购买数量
            )
            
            db.session.add(transaction)
            
            # 更新商品状态为已预订
            product.status = 'reserved'
            product.buyer_id = session['user_id']
            
            # 注意：不再在购买时减少商品数量，而是在交易完成时减少
            
            # 创建通知给卖家
            notification_message = f"您的商品「{product.name}」收到了一个新的购买请求。\n买家: {session['username']}\n数量: {quantity}\n总价: ¥{total_amount:.2f}\n收货地址: {address}\n买家联系方式: {contact_info}\n请在商品详情页面确认交易。"
            seller_notification = Notification(
                user_id=product.seller_id,
                message=notification_message
            )
            db.session.add(seller_notification)
            
            # 提交事务
            db.session.commit()
            
            # 发送购买通知给卖家（这里简单打印到控制台，实际应用中可以发送邮件或站内信）
            print(f"=== 新的购买请求通知 ===")
            print(f"商品名称: {product.name}")
            print(f"单价: ¥{product.price}")
            print(f"数量: {quantity}")
            print(f"总价: ¥{total_amount}")
            print(f"买家用户名: {session['username']}")
            print(f"买家学号: {session['user_id']}")
            print(f"收货地址: {address}")
            print(f"买家联系方式: {contact_info}")
            print(f"交易ID: {transaction.id}")
            print(f"手续费: ¥{transaction.fee}")
            print(f"卖家用户名: {product.seller.username}")
            print(f"卖家学号: {product.seller.student_id}")
            print(f"卖家邮箱: {product.seller.email}")
            print(f"==================")
            
            flash(f'购买请求已发送给卖家，请等待联系。总价: ¥{total_amount:.2f}')
            
            return redirect(url_for('product_detail', product_id=product_id))
        except Exception as e:
            db.session.rollback()
            flash('购买请求发送失败，请稍后重试')
            print(f"购买请求失败: {str(e)}")
            return redirect(url_for('product_detail', product_id=product_id))
    
    # GET请求时显示购买表单
    return render_template('buy_product.html', product=product, Notification=Notification)

@app.route('/transactions/<int:transaction_id>/pay', methods=['GET', 'POST'])
def pay_transaction(transaction_id):
    # 传递Notification模型到模板上下文
    """处理交易支付"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    transaction = Transaction.query.get_or_404(transaction_id)
    
    # 检查是否有权限支付此交易
    if session['user_id'] != transaction.buyer_id:
        flash('您无权支付此交易')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        payment_method = request.form['payment_method']
        
        # 创建支付订单
        order_id = f"ORDER_{transaction.id}_{int(datetime.utcnow().timestamp())}"
        description = f"购买商品: {transaction.product.name}"
        
        # 处理支付
        result = payment_processor.process_payment(
            payment_method, 
            transaction.amount + transaction.fee, 
            order_id, 
            description
        )
        
        if result['success']:
            # 重定向到支付页面
            return redirect(result['payment_url'])
        else:
            flash(f"支付失败: {result['message']}")
    
    return render_template('payment.html', transaction=transaction, Notification=Notification)

@app.route('/payment/success')
def payment_success():
    # 传递Notification模型到模板上下文
    """支付成功页面"""
    # 实际应用中应验证支付结果
    return render_template('payment_success.html', Notification=Notification)

@app.route('/payment/cancel')
def payment_cancel():
    # 传递Notification模型到模板上下文
    """支付取消页面"""
    return render_template('payment_cancel.html', Notification=Notification)

@app.route('/payment/wechat/notify', methods=['POST'])
def wechat_payment_notify():
    # 传递Notification模型到模板上下文
    """微信支付回调处理"""
    # 获取回调数据
    # 实际应用中应验证签名
    # data = request.get_data()
    # result = handle_payment_callback(data)
    
    # 模拟处理成功
    return "success"

@app.route('/payment/alipay/notify', methods=['POST'])
def alipay_payment_notify():
    # 传递Notification模型到模板上下文
    """支付宝支付回调处理"""
    # 获取回调数据
    # 实际应用中应验证签名
    # data = request.form.to_dict()
    # result = handle_payment_callback(data)
    
    # 模拟处理成功
    return "success"

# 计算手续费的函数
def calculate_fee(user_id):
    # 查询用户已完成的交易次数
    completed_transactions = Transaction.query.filter(
        Transaction.buyer_id == user_id,
        Transaction.status == 'completed'
    ).count()
    
    # 根据交易次数计算手续费
    if completed_transactions >= 10:
        return 0.01  # 10次以上手续费1分钱
    elif completed_transactions >= 5:
        return 0.05  # 5次以上手续费5分钱
    else:
        return 0.10  # 默认手续费1毛钱

@app.route('/transactions/<int:transaction_id>/complete', methods=['POST'])
def complete_transaction(transaction_id):
    # 传递Notification模型到模板上下文
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    transaction = Transaction.query.get_or_404(transaction_id)
    
    # 只有卖家可以完成交易
    if session['user_id'] != transaction.seller_id:
        flash('您无权操作此交易')
        return redirect(url_for('index'))
    
    # 更新交易状态
    transaction.status = 'completed'
    
    # 在交易完成时减少商品剩余数量
    print(f"交易完成前: 商品ID {transaction.product.id}, 原始剩余数量: {transaction.product.remaining_quantity}, 交易数量: {transaction.quantity}")
    transaction.product.remaining_quantity -= transaction.quantity
    print(f"交易完成后: 商品ID {transaction.product.id}, 剩余数量: {transaction.product.remaining_quantity}")
    
    # 如果剩余数量为0，将商品状态更新为已售出
    if transaction.product.remaining_quantity == 0:
        transaction.product.status = 'sold'
        transaction.product.sold_at = datetime.utcnow()
    
    try:
        db.session.commit()
        print(f"交易 {transaction_id} 已成功提交到数据库")
        flash('交易已完成，商品数量已更新。')
    except Exception as e:
        db.session.rollback()
        print(f"交易提交失败: {str(e)}")
        flash('交易完成失败，请稍后重试。')
    
    return redirect(url_for('product_detail', product_id=transaction.product.id))

@app.route('/reports/new/<int:transaction_id>', methods=['GET', 'POST'])
def new_report(transaction_id):
    # 传递Notification模型到模板上下文
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    transaction = Transaction.query.get_or_404(transaction_id)
    
    # 允许交易参与方举报
    if session['user_id'] not in [transaction.seller_id, transaction.buyer_id]:
        flash('您无权举报此交易')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        reason = request.form['reason']
        
        # 确定被举报用户
        reported_user_id = transaction.seller_id if session['user_id'] == transaction.buyer_id else transaction.buyer_id
        
        new_report = Report(
            reporter_id=session['user_id'],
            reported_user_id=reported_user_id,
            transaction_id=transaction_id,
            reason=reason
        )
        
        db.session.add(new_report)
        
        try:
            db.session.commit()
            flash('举报已提交，管理员会尽快处理')
            
            # 通知管理员有新的举报
            print(f"管理员通知：有新的举报提交，举报ID: {new_report.id}")
            
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash('举报提交失败，请稍后重试')
    
    return render_template('new_report.html', transaction=transaction, Notification=Notification)

@app.route('/admin')
def admin_panel():
    # 检查用户是否为管理员
    if 'user_id' not in session or not session.get('is_admin', False):
        flash('您无权访问管理员面板')
        return redirect(url_for('index'))
    
    reports = Report.query.filter_by(status='pending').all()
    # 获取最新的交易信息
    recent_transactions = Transaction.query.order_by(Transaction.created_at.desc()).limit(10).all()
    
    # 传递Product模型到模板上下文
    return render_template('admin_panel.html', 
                         reports=reports, 
                         transactions=recent_transactions,
                         Product=Product,
                         datetime=datetime,
                         timedelta=timedelta,
                         Notification=Notification)

@app.route('/admin/reports/<int:report_id>/resolve', methods=['POST'])
def resolve_report(report_id):
    # 传递Notification模型到模板上下文
    # 检查用户是否为管理员
    if 'user_id' not in session or not session.get('is_admin', False):
        flash('您无权执行此操作')
        return redirect(url_for('index'))
    
    report = Report.query.get_or_404(report_id)
    action = request.form['action']  # 'dismiss' 或 'ban'
    
    if action == 'ban':
        # 封禁被举报用户
        reported_user = User.query.get(report.reported_user_id)
        reported_user.is_blacklisted = True
    
    report.status = 'resolved'
    db.session.commit()
    
    flash('举报已处理')
    return redirect(url_for('admin_panel'))

@app.route('/admin/settings', methods=['GET', 'POST'])
def admin_settings():
    # 传递Notification模型到模板上下文
    # 检查用户是否为管理员
    if 'user_id' not in session or not session.get('is_admin', False):
        flash('您无权访问管理员面板')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        # 这里可以添加管理员修改平台设置的功能
        flash('设置已保存')
        return redirect(url_for('admin_settings'))
    
    return render_template('admin_settings.html', Notification=Notification)

@app.route('/admin/fee-test', methods=['GET', 'POST'])
def fee_test():
    # 传递Notification模型到模板上下文
    # 检查用户是否为管理员
    if 'user_id' not in session or not session.get('is_admin', False):
        flash('您无权访问此页面')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        user_id = int(request.form['user_id'])
        
        # 查询用户已完成的交易次数
        completed_transactions = Transaction.query.filter(
            Transaction.buyer_id == user_id,
            Transaction.status == 'completed'
        ).count()
        
        # 计算手续费
        fee = calculate_fee(user_id)
        
        return render_template('fee_test.html', 
                             user_id=user_id, 
                             transaction_count=completed_transactions, 
                             fee=fee,
                             Notification=Notification)
    
    return render_template('fee_test.html', Notification=Notification)

@app.route('/admin/users')
def user_list():
    # 传递Notification模型到模板上下文
    # 检查用户是否为管理员
    if 'user_id' not in session or not session.get('is_admin', False):
        flash('您无权访问此页面')
        return redirect(url_for('index'))
    
    page = request.args.get('page', 1, type=int)
    
    # 获取所有用户并分页
    users = User.query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False)
    
    return render_template('user_list.html', users=users.items, pagination=users, Notification=Notification)

@app.route('/admin/users/<int:user_id>/products')
def view_user_products(user_id):
    # 传递Notification模型到模板上下文
    # 检查用户是否为管理员
    if 'user_id' not in session or not session.get('is_admin', False):
        flash('您无权访问此页面')
        return redirect(url_for('index'))
    
    # 获取目标用户
    target_user = User.query.get_or_404(user_id)
    
    page = request.args.get('page', 1, type=int)
    
    # 获取该用户发布的所有商品并分页
    products = Product.query.filter_by(seller_id=user_id).order_by(Product.created_at.desc()).paginate(
        page=page, per_page=6, error_out=False)
    
    return render_template('user_products.html', 
                         target_user=target_user, 
                         products=products.items, 
                         pagination=products,
                         Notification=Notification)

@app.route('/admin/users/<int:user_id>/logout', methods=['POST'])
def admin_logout_user(user_id):
    # 检查用户是否为管理员
    if 'user_id' not in session or not session.get('is_admin', False):
        flash('您无权执行此操作')
        return redirect(url_for('index'))
    
    # 不能注销自己
    if user_id == session['user_id']:
        flash('不能注销自己的账号')
        return redirect(url_for('user_list'))
    
    # 获取目标用户
    user = User.query.get_or_404(user_id)
    
    # 不能注销其他管理员
    if user.is_admin:
        flash('不能注销管理员账号')
        return redirect(url_for('user_list'))
    
    # 注销用户（将其标记为已注销）
    user.is_blacklisted = True
    db.session.commit()
    
    flash(f'用户 {user.username} 的账号已被注销')
    return redirect(url_for('user_list'))

@app.route('/products/<int:product_id>/remove', methods=['POST'])
def remove_product(product_id):
    # 传递Notification模型到模板上下文
    """卖家下架自己的商品"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    product = Product.query.get_or_404(product_id)
    
    # 检查是否是商品所有者
    if session['user_id'] != product.seller_id:
        flash('您无权下架此商品')
        return redirect(url_for('index'))
    
    # 检查商品状态是否可以下架
    if product.status != 'available':
        flash('只有可购买状态的商品才能下架')
        return redirect(url_for('product_detail', product_id=product_id))
    
    # 下架商品
    product.status = 'removed'
    db.session.commit()
    
    flash('商品已成功下架')
    return redirect(url_for('product_detail', product_id=product_id))

@app.route('/admin/products/<int:product_id>/remove', methods=['POST'])
def admin_remove_product(product_id):
    # 传递Notification模型到模板上下文
    """管理员强制下架任何商品"""
    if 'user_id' not in session or not session.get('is_admin', False):
        flash('您无权执行此操作')
        return redirect(url_for('index'))
    
    product = Product.query.get_or_404(product_id)
    
    # 检查商品状态是否可以下架
    if product.status == 'sold':
        flash('已售出的商品无法下架')
        return redirect(url_for('product_detail', product_id=product_id))
    
    # 下架商品
    product.status = 'removed'
    db.session.commit()
    
    flash('商品已被管理员强制下架')
    return redirect(url_for('product_detail', product_id=product_id))

@app.route('/notifications')
def notifications():
    # 传递Notification模型到模板上下文
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    page = request.args.get('page', 1, type=int)
    
    # 获取当前用户的通知并分页
    user_notifications = Notification.query.filter_by(user_id=session['user_id'])\
        .order_by(Notification.created_at.desc())\
        .paginate(page=page, per_page=10, error_out=False)
    
    return render_template('notifications.html', 
                         notifications=user_notifications.items,
                         pagination=user_notifications,
                         Notification=Notification)

@app.route('/notifications/<int:notification_id>/read', methods=['POST'])
def mark_notification_read(notification_id):
    # 传递Notification模型到模板上下文
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    notification = Notification.query.get_or_404(notification_id)
    
    # 检查是否是当前用户的通知
    if notification.user_id != session['user_id']:
        flash('您无权操作此通知')
        return redirect(url_for('notifications'))
    
    notification.is_read = True
    db.session.commit()
    
    return redirect(url_for('notifications'))

@app.route('/notifications/read-all', methods=['POST'])
def mark_all_notifications_read():
    # 传递Notification模型到模板上下文
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # 将所有未读通知标记为已读
    Notification.query.filter_by(user_id=session['user_id'], is_read=False)\
        .update({Notification.is_read: True})
    db.session.commit()
    
    flash('所有通知已标记为已读')
    return redirect(url_for('notifications'))

@app.route('/profile')
def profile():
    # 传递Notification模型到模板上下文
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    return render_template('profile.html', current_user=user, Notification=Notification)

@app.route('/update_username', methods=['POST'])
def update_username():
    # 传递Notification模型到模板上下文
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    new_username = request.form.get('new_username', '').strip()
    
    # 验证用户名
    if not new_username or len(new_username) < 3 or len(new_username) > 20:
        flash('用户名长度应在3-20个字符之间')
        return redirect(url_for('profile'))
    
    # 检查用户名是否已存在
    existing_user = User.query.filter(
        User.username == new_username,
        User.id != user.id
    ).first()
    
    if existing_user:
        flash('该用户名已被其他用户使用')
        return redirect(url_for('profile'))
    
    # 更新用户名
    old_username = user.username
    user.username = new_username
    db.session.commit()
    
    # 更新会话中的用户名
    session['username'] = new_username
    
    flash(f'用户名已从 "{old_username}" 更新为 "{new_username}"')
    return redirect(url_for('profile'))

# 图片优化函数
def optimize_image(image_file, save_path):
    """优化上传的图片"""
    try:
        # 打开图片
        img = Image.open(image_file)
        
        # 转换为RGB模式（如果需要）
        if img.mode in ('RGBA', 'LA', 'P'):
            img = img.convert('RGB')
        
        # 调整图片大小（最大宽度800px）
        max_width = 800
        if img.width > max_width:
            ratio = max_width / img.width
            new_height = int(img.height * ratio)
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
        
        # 保存图片，质量设为85%
        img.save(save_path, 'JPEG', quality=85, optimize=True)
    except Exception as e:
        # 如果优化失败，直接保存原图
        image_file.seek(0)
        image_file.save(save_path)

# 导入支付模块
from payment import PaymentProcessor

# 初始化支付处理器
payment_processor = PaymentProcessor()

def cleanup_sold_products():
    """后台任务：定期清理24小时前已售出的商品"""
    with app.app_context():
        while True:
            try:
                # 计算24小时前的时间
                cutoff_time = datetime.utcnow() - timedelta(hours=24)
                
                # 查找24小时前已售出的商品
                old_sold_products = Product.query.filter(
                    Product.status == 'sold',
                    Product.sold_at < cutoff_time
                ).all()
                
                # 为每个过期商品创建管理员备份记录并删除
                for product in old_sold_products:
                    print(f"商品已过期24小时，正在清理: {product.name} (ID: {product.id})")
                    # 创建备份记录供管理员查看（简化处理）
                    # 在实际应用中，您可能需要将数据移动到另一个表中
                    
                    # 注意：这里我们不实际删除商品，而是保留它们供管理员查看历史记录
                    # 如果需要真正删除，可以取消下面的注释
                    # db.session.delete(product)
                
                if old_sold_products:
                    db.session.commit()
                    print(f"已清理 {len(old_sold_products)} 个过期商品")
                
                print(f"商品清理任务完成，检查时间: {datetime.utcnow()}")
                
            except Exception as e:
                print(f"商品清理任务出错: {e}")
            
            # 每小时检查一次
            time.sleep(3600)

# 在应用启动时启动后台任务
def start_background_tasks():
    """启动后台任务"""
    # 启动商品清理任务
    cleanup_thread = threading.Thread(target=cleanup_sold_products, daemon=True)
    cleanup_thread.start()

def get_network_info():
    """获取详细的网络信息"""
    info = {}
    
    # 获取主机名
    info['hostname'] = socket.gethostname()
    
    # 获取所有网络接口IP
    try:
        # 使用ipconfig命令获取网络信息（Windows）
        result = subprocess.run(['ipconfig'], capture_output=True, text=True, shell=True)
        output = result.stdout
        
        # 提取IPv4地址
        ipv4_pattern = r'IPv4 Address[.\s]*:\s*(\d+\.\d+\.\d+\.\d+)'
        ipv4_matches = re.findall(ipv4_pattern, output)
        info['ipv4_addresses'] = ipv4_matches
    except Exception as e:
        info['error'] = str(e)
        info['ipv4_addresses'] = []
    
    return info

def get_local_ip():
    """获取本机在局域网中的IP地址"""
    try:
        # 创建一个UDP socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 连接到一个远程地址（这里使用Google的DNS）
        s.connect(("8.8.8.8", 80))
        # 获取本地IP地址
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        # 如果无法获取，则返回默认值
        return "127.0.0.1"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    start_background_tasks()
    
    # 检查是否在生产环境
    if os.environ.get('FLASK_ENV') == 'production':
        # 生产环境配置
        app.config['DEBUG'] = False
        host = '0.0.0.0'
        port = int(os.environ.get('PORT', 5000))
    else:
        # 开发环境配置
        # 获取网络信息
        local_ip = get_local_ip()
        network_info = get_network_info()
        
        print("=" * 50)
        print("校园交易平台服务器启动成功！")
        print("=" * 50)
        print(f"本地访问: http://localhost:5000")
        print(f"局域网访问: http://{local_ip}:5000")
        
        # 显示所有可用的IP地址
        if 'ipv4_addresses' in network_info and network_info['ipv4_addresses']:
            print("\n所有可用的局域网地址:")
            for ip in network_info['ipv4_addresses']:
                print(f"  - http://{ip}:5000")
        
        print("\n访问说明:")
        print("1. 同一局域网内的设备可以直接使用上述地址访问")
        print("2. 要从外部网络（互联网）访问，需要配置路由器端口转发")
        print("3. 端口转发设置：将外部端口5000转发到本机IP的5000端口")
        print("4. 如果使用防火墙，请确保5000端口已开放")
        print("=" * 50)
        
        host = '0.0.0.0'
        port = 5000
    
    app.run(debug=True, host=host, port=port)

# 添加文件类型验证函数
def allowed_file(filename):
    """验证允许的文件类型"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    """验证允许的文件类型"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
