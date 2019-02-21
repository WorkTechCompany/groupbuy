from application import db, app
from sqlalchemy import Integer, Column, DateTime, String, DECIMAL
from sqlalchemy.schema import FetchedValue

class CustomerLogin(db.Model):
    __tablename__ = 'customer_login'

    Cid = db.Column(db.BigInteger, primary_key=True)                                                   # 顾客ID
    CustomerPhone = db.Column(db.String(20), primary_key=True)                                         # 顾客手机号
    CustomerPassword = db.Column(db.String(36), nullable=False, server_default=db.FetchedValue())     # 支付密码
    Password_salt = db.Column(db.String(36), nullable=False, server_default=db.FetchedValue())     # 登录密码随机密钥
    CustomerPayword = db.Column(db.String(36), nullable=False, server_default=db.FetchedValue())     # 支付密码
    Payword_salt = db.Column(db.String(36), nullable=False, server_default=db.FetchedValue())     # 支付密码随机密钥
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    openid = db.Column(db.String(80), nullable=False, server_default=db.FetchedValue())


