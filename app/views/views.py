from flask import render_template, request, url_for, redirect, session
from flask.wrappers import Request
from config import flaskConfig
from ..db.db import User, db
import hashlib

class viewFunctions:

    """
        网站主页
    """
    @flaskConfig.app.route('/')
    def index():
        # 检测session是否存在email，如果不存在就是未登陆，转到登陆页面，存在的话转到控制台
        if session.get('email') == None:
            return redirect('/login')
        else:
            return redirect('/dashboard')
    
    """
        控制台主页
    """
    @flaskConfig.app.route('/dashboard')
    def dashboard():
        if session.get('email') == None:
            return redirect('/login')
        else:
            return render_template('index.html', title="控制台 - 蘑菇丁自动云")

    """
        登陆页面处理方法
    """
    @flaskConfig.app.route('/login', methods=['get', 'POST'])
    def login():
        if request.method == 'POST':
            # 接受POST表单值
            email = request.form['email']
            password = request.form['password']
            md5 = hashlib.md5()
            md5.update(bytes(password.encode()))
            password = md5.hexdigest()

            # 将拿到的值做条件筛查
            userList = User.query.filter_by(email=email, password=password).first()
            if userList:
                if userList.id != None:
                    session['email'] = email
                    return redirect('/')
                # 设置session，转入控制台
                pass
            else:
                return render_template('login.html', alert="请检查登陆信息是否正确，登陆失败！", title="登陆 - 蘑菇丁自动云")

        # 如果已经存在email session，转入控制台
        if session.get('email') != None:
            return redirect('/dashboard')
        return render_template('login.html', title="登陆 - 蘑菇丁自动云")
    
    """
        注册页面处理方法
    """
    @flaskConfig.app.route('/register', methods=['get', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            repeatPassword = request.form['repeatPassword']
            alert = ""

            if username != '' and len(username) < 10 and password == repeatPassword:
                md5 = hashlib.md5()
                md5.update(bytes(password.encode()))
                createUser = User(username=username, email=email, password=md5.hexdigest())
                db.session.add_all([createUser])
                db.session.commit()

            elif username == '' or email == '' or password == '' or repeatPassword == '':
                alert = "请检查信息的完整性"
            
            else:
                alert = "未知错误！"

            return redirect('/login')
        else:
            if session.get('email') != None:
                return redirect('/dashboard')
            return render_template('register.html')

    """
        登出处理方法
    """
    @flaskConfig.app.route('/logout')
    def logout():
        # 清除session
        session.clear()
        return redirect('/login')
    
    """
        404
    """
    @flaskConfig.app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html', title="哦不！页面不见了！"), 404