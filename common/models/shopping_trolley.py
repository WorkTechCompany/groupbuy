from application import db, app
from sqlalchemy import Integer, Column, DateTime, String, DECIMAL, TEXT
from sqlalchemy.schema import FetchedValue


class ShoppingTrolley(db.Model):
    __tablename__ = 'shopping_trolley'

    Id = db.Column(db.BigInteger, primary_key=True)                                                        # id号码
    Cid = db.Column(db.BigInteger, nullable=False, server_default=db.FetchedValue())              # 顾客ID
    ShopId = db.Column(db.BigInteger, nullable=False, server_default=db.FetchedValue())                     # 商店ID
    ShopName = db.Column(db.String(128), nullable=False, server_default=db.FetchedValue())                        # 商店名称
    ProductName = db.Column(db.String(128), nullable=False, server_default=db.FetchedValue())        # 商品名称
    Count = db.Column(db.BigInteger, nullable=False, server_default=db.FetchedValue())           # 数量
    ProdectPrice = db.Column(DECIMAL, nullable=False, server_default=db.FetchedValue())                    # 商品价格
    ProductFormat = db.Column(TEXT, nullable=False, server_default=db.FetchedValue())                       # 商品规格

