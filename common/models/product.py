from application import db, app
from sqlalchemy import Integer, Column, DateTime, String, DECIMAL, TEXT
from sqlalchemy.schema import FetchedValue


class Product(db.Model):
    __tablename__ = 'productinfo'

    PId = db.Column(db.BigInteger, primary_key=True)                                                        # 商品ID
    ProductName = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())              # 商品名称
    ShopId = db.Column(db.BigInteger, nullable=False, server_default=db.FetchedValue())                     # 商店ID
    AId = db.Column(db.BigInteger, nullable=False, server_default=db.FetchedValue())                        # 商户ID
    ProductMerchanName = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())        # 商品店主名字
    ProductCategory = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())           # 商品分类
    ProductInfo = db.Column(db.String(5000), nullable=False, server_default=db.FetchedValue())             # 商品信息
    ProductSold = db.Column(Integer, nullable=False, server_default=db.FetchedValue())                     # 商品已售数
    Productsku = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())           # 商品规格
    ProductFormat = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())           # 商品规格
    ProductImage = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())           # 商品图片
    ProductAttributes = db.Column(db.BigInteger, nullable=False, server_default=db.FetchedValue())      # 销售属性
    ProductProvince = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())            # 省份
    ProductCity = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())                # 市区
    ProductCountry = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())               # 县

