from application import db, app
from sqlalchemy import Integer, Column, DateTime, String, DECIMAL
from sqlalchemy.schema import FetchedValue

class Customer(db.Model):
    __tablename__ = 'customer'

    Cid = db.Column(db.BigInteger, nullable=False, server_default=db.FetchedValue())                   # 顾客ID
    CustomerName = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())         # 顾客名字
    CustomerPhone = db.Column(db.String(20), primary_key=True)                                         # 顾客手机号
    MyBalance = db.Column(DECIMAL, nullable=False, server_default=db.FetchedValue())             # 我的余额
    AvailableBalance = db.Column(DECIMAL, nullable=False, server_default=db.FetchedValue())    # 可用余额
    MyIncome = db.Column(DECIMAL, nullable=False, server_default=db.FetchedValue())              # 我的收益


