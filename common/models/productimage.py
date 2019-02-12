from application import db, app
from sqlalchemy import Integer, Column, DateTime, String, DECIMAL, TEXT
from sqlalchemy.schema import FetchedValue


class Productimage(db.Model):
    __tablename__ = 'productimage'

    id = db.Column(db.BigInteger, primary_key=True)                                                        # id
    PId = db.Column(Integer, nullable=False, unique=True, server_default=db.FetchedValue())               #  商品ID
    ProductImage = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())           # 商品图片
