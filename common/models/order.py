from application import db, app
from sqlalchemy import Integer, Column, DateTime, String, DECIMAL
from sqlalchemy.schema import FetchedValue

class Order(db.Model):
    __tablename__ = 'order'

    Oid = db.Column(db.BigInteger, primary_key=True)                                         # 订单ID
    Pid = db.Column(db.BigInteger, nullable=False, server_default=db.FetchedValue())         # 商品ID
    Cid = db.Column(db.BigInteger, nullable=False, server_default=db.FetchedValue())         # 顾客ID
    ProductName = db.Column(db.String(20), primary_key=True)                                         # 商品名称
    ProductImage = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())             # 商品图片
    ProdectPrice = db.Column(DECIMAL, nullable=False, server_default=db.FetchedValue())             # 商品价格
    OrderTime = db.Column(DateTime, nullable=False, index=True, server_default=FetchedValue())          # 下单时间
    OrderStatus = db.Column(Integer, nullable=False, server_default=db.FetchedValue())                     # 订单状态  1为已发货


