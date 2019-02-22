from application import db, app
from sqlalchemy import Integer, Column, DateTime, String, DECIMAL, TEXT
from sqlalchemy.schema import FetchedValue


class Images(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.BigInteger, primary_key=True)                                                        # id
    images = db.Column(TEXT, nullable=False, server_default=db.FetchedValue())           # 图片
    info = db.Column(TEXT, nullable=False, server_default=db.FetchedValue())           # 字

