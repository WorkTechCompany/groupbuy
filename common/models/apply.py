from application import db, app
from sqlalchemy import Integer, Column, DateTime, String, DECIMAL
from sqlalchemy.schema import FetchedValue


class Apply(db.Model):
    __tablename__ = 'apply'

    Aid = db.Column(db.BigInteger, primary_key=True)                                                       # 商铺id号码
    ShopCategory = db.Column(db.BigInteger, primary_key=True)                                              # 实体店属性
    IdentityCard = db.Column(db.String(500), nullable=False, server_default=db.FetchedValue())              # 身份证正面照片
    IdentityCardHand = db.Column(db.String(500), nullable=False, server_default=db.FetchedValue())          # 手持身份证
    BusinessLicense= db.Column(db.String(500), nullable=False, server_default=db.FetchedValue())          # 营业执照
    Contract = db.Column(db.String(500), nullable=False, server_default=db.FetchedValue())                        # 合同
    IDCard = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())                   # 身份证号码（户名）
    ApplyProvince = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())            # 省份
    ApplyCity = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())                  # 市区
    ApplyCounty = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())               # 县
    ApplyDetails = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())             # 地址详细
    ApplyPhone  = db.Column(Integer, nullable=False, unique=True, server_default=db.FetchedValue())        # 手机号（工号）
    ApplyPassword = db.Column(Integer, nullable=False, server_default=db.FetchedValue())                   # 密码
    ApplyStatus = db.Column(Integer, nullable=False, server_default=db.FetchedValue())                     # 审核状态  1为已过审