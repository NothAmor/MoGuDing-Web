from enum import unique
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from config import flaskConfig
import pymysql
pymysql.install_as_MySQLdb()

class dbConfig(object):
    # 上线数据库
    # server = '47.101.38.190:3306'
    # user = 'moguding'
    # password = 'yfmPTJpHDWtSxsMM'
    # database = 'moguding'

    # 测试环境数据库
    server = '47.101.38.190:3306'
    user = 'moguding-web'
    password = 'Tm88wtk2pTSmmNDA'
    database = 'moguding-web'
    flaskConfig.app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s/%s' % (user, password, server, database)
    
    # 设置sqlalchemy自动跟踪数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 查询时显示原始SQL语句
    flaskConfig.app.config['SQLALCHEMY_ECHO'] = True

    # 禁止自动提交数据处理
    flaskConfig.app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False

db = SQLAlchemy(flaskConfig.app)

"""
    用户表
"""
class User(db.Model):
    # 表名
    __tablename__ = 'users'

    # 字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64))
    email = db.Column(db.String(255), unique=True, index=True)
    password = db.Column(db.String(255))
    rmb = db.Column(db.Integer, default=50)

"""
    蘑菇丁账户表
"""
class mogudingAccount(db.Model):
    # 表名
    __tablename__ = 'mogudingAccount'

    # 字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner = db.Column(db.String(255))
    phoneNumber = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    token = db.Column(db.String(2555))
    userAgent = db.Column(db.String(2555))
    userId = db.Column(db.String(255))
    remark = db.Column(db.String(255))

"""
    蘑菇丁打卡地址表
"""
class mogudingAddress(db.Model):
    # 表名
    __tablename__ = 'mogudingAddress'

    # 字段
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner = db.Column(db.String(255))
    phoneNumber = db.Column(db.String(255))
    province = db.Column(db.String(255))
    city = db.Column(db.String(255))
    detailedAddress = db.Column(db.String(2555))
    longitude = db.Column(db.String(255))
    latitude = db.Column(db.String(255))

"""
    打卡任务数据表
"""
class mogudingTasks(db.Model):
    __tablename__ = 'mogudingTasks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner = db.Column(db.String(255))
    taskType = db.Column(db.String(255))
    runAccount = db.Column(db.String(255))
    runGoalId = db.Column(db.String(255))
    runGoalName = db.Column(db.String(2555))
    runRule = db.Column(db.String(255))
    runTime = db.Column(db.String(255))
    deviceType = db.Column(db.String(255))
    status = db.Column(db.Boolean)
    description = db.Column(db.String(2555))

"""
    任务日志
"""
class mogudingLogs(db.Model):
    __tablename__ = 'mogudingLogs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner = db.Column(db.String(255))
    taskType = db.Column(db.String(255))
    account = db.Column(db.String(255))
    goal = db.Column(db.String(255))
    runTime = db.Column(db.String(255))
    taskTime = db.Column(db.String(255))
    taskResult = db.Column(db.Boolean)
    failReason = db.Column(db.String(2555))

"""
    打卡任务信息推送
"""
class mogudingTaskSend(db.Model):
    __tablename__ = 'mogudingTaskSend'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner = db.Column(db.String(255))
    account = db.Column(db.String(255))
    sendKey = db.Column(db.String(255))