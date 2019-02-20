# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, Numeric
from sqlalchemy.schema import FetchedValue
# from common.models.member.Member import Member
from application import db


class ShopSaleChangeLog(db.Model):
    __tablename__ = 'shop_sale_change_log'

    id = db.Column(db.Integer, primary_key=True)
    Pid = db.Column(db.Integer, nullable=False, index=True, server_default=db.FetchedValue())
    quantity = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    price = db.Column(db.Numeric(10, 2), nullable=False, server_default=db.FetchedValue())
    Cid = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())

    # @property
    # def member_name(self):
    #     member = Member.query.filter_by(id= self.member_id).first()
    #     return member.nickname


