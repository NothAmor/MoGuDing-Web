from flask import render_template, request, url_for, redirect, session
from flask.wrappers import Request
from config import flaskConfig
from ..db.db import User, mogudingAccount, db

import hashlib
import random

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
            return render_template('index.html', title="控制台 - {}".format(flaskConfig.websiteName), username=session['username'])

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
                    session['username'] = userList.username
                    return redirect('/')
                # 设置session，转入控制台
                pass
            else:
                return render_template('login.html', alert="请检查登陆信息是否正确，登陆失败！", title="登陆 - {}".format(flaskConfig.websiteName))

        # 如果已经存在email session，转入控制台
        if session.get('email') != None:
            return redirect('/dashboard')
        return render_template('login.html', title="登陆 - {}".format(flaskConfig.websiteName))
    
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

            userList = User.query.filter_by(email=email).first()
            if username != '' and len(username) < 10 and password == repeatPassword and userList == None:
                md5 = hashlib.md5()
                md5.update(bytes(password.encode()))
                createUser = User(username=username, email=email, password=md5.hexdigest())
                db.session.add_all([createUser])
                db.session.commit()
                
                return redirect('/login')

            elif username == '' or email == '' or password == '' or repeatPassword == '':
                alert = "请检查信息的完整性"
            elif userList != None:
                alert = "该电子邮件已经注册，请登陆！"
            else:
                alert = "未知错误！"

            return render_template('register.html', title="注册 - {}".format(flaskConfig.websiteName), alert=alert)
        else:
            if session.get('email') != None:
                return redirect('/dashboard')
            return render_template('register.html', title="注册 - {}".format(flaskConfig.websiteName))

    """
        登出处理方法
    """
    @flaskConfig.app.route('/logout')
    def logout():
        # 清除session
        session.clear()
        return redirect('/login')

    """
        账户管理页面
    """
    @flaskConfig.app.route('/accountManage', methods=['get', 'POST'])
    def accountManage():
        if request.method == 'POST':
            phoneNumber = request.form['phoneNumber']
            password = request.form['password']
            token = request.form['token']
            userAgent = request.form['userAgent']
            remark = request.form['remark']
            alert = ""

            phoneNumberUniqueQuery = mogudingAccount.query.filter_by(phoneNumber=phoneNumber).first()
            if phoneNumberUniqueQuery != None:
                alert = "该蘑菇丁账户已经在平台内被绑定！如果你是此账户的实际持有者，请发邮件申诉！"
                return render_template('accountManage.html', title="账户管理 - {}".format(flaskConfig.websiteName), username=session['username'],
                                        alert=alert)
            if phoneNumber != "" and password != "" and remark != "":
                if userAgent == "":
                    userAgent = flaskConfig.userAgents[random.randint(0, len(flaskConfig.userAgents) - 1)]
                addMoGuDingAccount = mogudingAccount(owner=session['email'], phoneNumber=phoneNumber, password=password, token=token,
                                                     userAgent=userAgent, remark=remark)
                db.session.add_all([addMoGuDingAccount])
                db.session.commit()
                accountQuery = mogudingAccount.query.filter_by(owner=session['email']).all()
                return render_template('accountManage.html', title="账户管理 - {}".format(flaskConfig.websiteName), username=session['username'],
                                        alert=alert, accountQuery=accountQuery)
            pass
        else:
            accountQuery = mogudingAccount.query.filter_by(owner=session['email']).all()
            return render_template('accountManage.html', title="账户管理 - {}".format(flaskConfig.websiteName), username=session['username'],
                                    accountQuery=accountQuery)
    
    """
        404
    """
    @flaskConfig.app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html', title="哦不！页面不见了！"), 404