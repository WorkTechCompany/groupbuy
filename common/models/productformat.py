from application import db, app
from sqlalchemy import Integer, Column, DateTime, String, DECIMAL, TEXT
from sqlalchemy.schema import FetchedValue


class ProductFormat(db.Model):
    __tablename__ = 'productformat'

    id = db.Column(db.BigInteger, primary_key=True)                                                        # id
    PId = db.Column(Integer, nullable=False, unique=True, server_default=db.FetchedValue())               #  商品ID
    ProductFormat = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())           # 商品规格
    ProdectPrice = db.Column(DECIMAL, nullable=False, server_default=db.FetchedValue())                    # 商品价格
    ProductStock = db.Column(Integer, nullable=False, unique=True, server_default=db.FetchedValue())      # 商品库存

