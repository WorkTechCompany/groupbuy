from application import db, app
from sqlalchemy import Integer, Column, DateTime, String, DECIMAL
from sqlalchemy.schema import FetchedValue


class Product(db.Model):
    __tablename__ = 'product_info'

    Id = db.Column(db.BigInteger, primary_key=True)                                                        # id号码
    ProductName = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())              # 商品名称
    ShopId = db.Column(db.BigInteger, primary_key=True)                                         # 商品店主ID
    ProductMerchanName = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())        # 商品店主名字
    ProductCategory = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())           # 商品分类
    ProductInfo = db.Column(db.String(5000), nullable=False, server_default=db.FetchedValue())             # 商品信息
    ProdectPrice = db.Column(DECIMAL, nullable=False, server_default=db.FetchedValue())                    # 商品价格
    ProductImage = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())             # 商品图片
    ProductStock  = db.Column(Integer, nullable=False, unique=True, server_default=db.FetchedValue())      # 商品库存
    ProductSold = db.Column(Integer, nullable=False, server_default=db.FetchedValue())                     # 商品已售数
    ProductStatus = db.Column(Integer, nullable=False, server_default=db.FetchedValue())                   # 商品状态  1为已过审


