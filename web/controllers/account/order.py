from web.controllers.account import route_account
from flask import jsonify, request, redirect
from common.models.product import Product
from common.libs.UrlManager import UrlManager
from common.models.order import Order
from common.models.address import Address
from common.libs.Helper import getFormatDate
from sqlalchemy import or_
import os
from application import app, db
import time


@route_account.route("/showorder/", methods=['POST'])
def showorder():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values

    page = int(req['page']) if 'page' in req else 1
    Shopid = int(req['Shopid']) if 'Shopid' in req else 0
    OrderStatus = int(req['OrderStatus']) if 'OrderStatus' in req else -1
    info = str(req['mix_kw']) if 'mix_kw' in req else ''

    if page < 1:
        page = 1

    page_size = 10
    offset = (page - 1) * page_size
    query = Order.query.filter_by()

    check = [-1, 0]
    if Shopid not in check and Shopid:
        query = Order.query.filter_by(Shopid=Shopid)

    if OrderStatus != -1 and OrderStatus:
        if OrderStatus == 4:
            query = Order.query.filter_by(OrderRefundStatus=2)
        elif OrderStatus == 5:
            query = Order.query.filter_by(OrderRefundStatus=1)
        else:
            query = Order.query.filter_by(OrderStatus=OrderStatus)

    if info:
        rule = or_(Order.Oid.ilike("%{0}%".format(info)))
        query = query.filter(rule)

    totalCount = query.count()

    apply_list = query.order_by(Order.Oid.desc()) \
        .offset(offset).limit(page_size).all()


    data_list = []
    if apply_list:
        for item in apply_list:
            if item.OrderRefundStatus == 2:
                OrderStatus = 4
            else:
                OrderStatus = item.OrderStatus
            tmp_data = {
                'Oid': item.Oid,
                'Pid': item.Pid,
                'Cid': item.Cid,
                'Shopid': item.Shopid,
                'ProductName': str(item.ProductName),
                'OrderCount': str(item.OrderCount),
                # 'OrderFormat': str(item.OrderFormat),
                'ProductImage': str(item.ProductImage),
                'OrderPrice': str(item.OrderPrice),
                'OrderTime': str(item.OrderTime),
                'OrderStatus': str(OrderStatus),
                'OrderRefundStatus': str(item.OrderRefundStatus),
                'OrderExpress': str(item.OrderExpress)
            }
            data_list.append(tmp_data)
    resp['totalCount'] = totalCount
    resp['data']['list'] = data_list
    resp['data']['has_more'] = 0 if len(data_list) < page_size else 1
    response = jsonify(resp)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@route_account.route("/orderinfo/", methods=['POST'])
def orderinfo():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values

    Oid = int(req['Oid']) if 'Oid' in req else -1

    OrderInfo = Order.query.filter_by(Oid=Oid).first()


    if OrderInfo:
        AddressInfo = OrderInfo.OrderAddress
        AddressInfo = Address.query.filter_by(Id=AddressInfo).first()

        address = {
            'id': AddressInfo.Id,
            'Cid': AddressInfo.Cid,
            'Addressee': AddressInfo.Addressee,
            'AddresseePhone': AddressInfo.AddresseePhone,
            'Province': AddressInfo.Province,
            'City': AddressInfo.City,
            'County': AddressInfo.County,
            'Details': AddressInfo.Details,
            'Status': int(AddressInfo.Status)
        }
        # if OrderInfo.OrderRefundStatus == 2:
        #     OrderStatus = 4
        # else:
        OrderStatus = OrderInfo.OrderStatus
        tmp_data = {
            'Oid': OrderInfo.Oid,
            'Pid': OrderInfo.Oid,
            'Cid': OrderInfo.Cid,
            'Shopid': OrderInfo.Shopid,
            'ProductName': "%s" % (OrderInfo.ProductName),
            'OrderCount': "%s" % (OrderInfo.OrderCount),
            'ProductImage': "%s" % (OrderInfo.ProductImage),
            'OrderPrice': "%s" % (OrderInfo.OrderPrice),
            'OrderTime': getFormatDate(OrderInfo.OrderTime),
            'OrderRefund': OrderInfo.OrderRefund,
            'OrderRefundStatus': OrderInfo.OrderRefundStatus,
            'OrderStatus': int(OrderStatus),
            'OrderAddressInfo': address
        }
        resp['data'] = tmp_data
    response = jsonify(resp)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

# 退款审核
@route_account.route("/order_refund/", methods=['POST'])
def order_refund():
    resp = {'code': 200, 'msg': '操作成功'}

    Oid = request.values['Oid'] if 'Oid' in request.values else -1
    OrderStatus = request.values['OrderStatus'] if 'OrderStatus' in request.values else 0
    OrderRefundStatus = request.values['OrderRefundStatus'] if 'OrderRefundStatus' in request.values else 0
    result = Order.query.filter_by(Oid=Oid).first()
    result.OrderRefundStatus = int(OrderRefundStatus)
    result.OrderStatus = int(OrderStatus)

    db.session.commit()
    response = jsonify(resp)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
