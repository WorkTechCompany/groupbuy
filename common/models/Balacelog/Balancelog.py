from application import db, app
from sqlalchemy import Integer, Column, DateTime, String, DECIMAL
from sqlalchemy.schema import FetchedValue

class Balancelog(db.Model):
    __tablename__ = 'balance_log'

    id = db.Column(db.BigInteger, primary_key=True)                                                   # id号
    Cid = db.Column(db.BigInteger, nullable=False, server_default=db.FetchedValue())         # 顾客ID
    createtime = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())           # 创建时间
    balance = db.Column(DECIMAL, nullable=False, server_default=db.FetchedValue())                    # 交易金额
    status = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())           # 状态
    operating = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())           # 操作
    total_balance = db.Column(DECIMAL, nullable=False, server_default=db.FetchedValue())              # 总金额
    receipt_qrcode = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())      # 收据码
    freeze_balance = db.Column(DECIMAL, nullable=False, server_default=db.FetchedValue())             # 冻结金额
    updatetime = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())             # 创建时间
    BankCardNumber = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())      # 银行卡号
    Openingbank = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())         # 开户行
    Accountname = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())         # 开户名


