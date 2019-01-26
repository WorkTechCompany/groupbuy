from application import db, app
from sqlalchemy import Integer, Column, DateTime, String, DECIMAL
from sqlalchemy.schema import FetchedValue

class Address(db.Model):
    __tablename__ = 'address'

    Id = db.Column(db.BigInteger, primary_key=True)                                                    # ID号码
    Cid = db.Column(db.BigInteger, nullable=False, server_default=db.FetchedValue())                   # 顾客ID
    Addressee = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())            # 收件人姓名
    AddresseePhone = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())       # 收件人电话
    Province = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())             # 省份
    City = db.Column(db.String(20), primary_key=True)                                                  # 市区
    County = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())                # 县
    Details = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())              # 地址详细
    Status = db.Column(Integer, nullable=False, server_default=db.FetchedValue())                      # 是否为默认地址  1位默认


