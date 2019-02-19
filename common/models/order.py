from application import db, app
from sqlalchemy import Integer, Column, DateTime, String, DECIMAL
from sqlalchemy.schema import FetchedValue

class Order(db.Model):
    __tablename__ = 'order'

    Oid = db.Column(db.BigInteger, primary_key=True)                                         # 订单号
    Pid = db.Column(db.BigInteger, nullable=False, server_default=db.FetchedValue())         # 商品ID
    Cid = db.Column(db.BigInteger, nullable=False, server_default=db.FetchedValue())         # 顾客ID
    Shopid = db.Column(db.BigInteger, nullable=False, server_default=db.FetchedValue())         # 店铺id
    ProductName = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())   # 商品名称
    OrderCount = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())      # 下单数量
    # OrderFormat = db.Column(db.String(100),nullable=False, server_default=db.FetchedValue())   # 下单规格
    ProductImage = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())             # 商品图片
    OrderPrice = db.Column(DECIMAL, nullable=False, server_default=db.FetchedValue())             # 下单价格
    OrderTime = db.Column(DateTime, nullable=False, index=True, server_default=FetchedValue())          # 下单时间
    OrderStatus = db.Column(Integer, nullable=False, server_default=db.FetchedValue())       # 订单状态  1为待付款  2为待收货  3为已完成 4为申请退款  5为退款成功
    OrderExpress = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())             # 订单快递
    OrderRefund = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())             # 退款理由
    OrderAddress = db.Column(db.BigInteger, nullable=False, server_default=db.FetchedValue())             # 订单收货地址
    OrderRefundStatus = db.Column(db.BigInteger, nullable=False, server_default=db.FetchedValue())             # 退款状态 0为无 -1为不同意 1为同意
