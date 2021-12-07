from enum import unique
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import flaskConfig
import pymysql
pymysql.install_as_MySQLdb()

class dbConfig(object):
    server = '47.101.38.190:3306'
    user = 'moguding'
    password = 'yfmPTJpHDWtSxsMM'
    database = 'moguding'
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
    token = db.Column(db.String(255))
    userAgent = db.Column(db.String(255))
    remark = db.Column(db.String(255))