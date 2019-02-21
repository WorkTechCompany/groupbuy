from web.controllers.account import route_account
from flask import jsonify, request, redirect
from common.models.product import Product
from common.libs.UrlManager import UrlManager
from common.models.Balacelog.Balancelog import Balancelog
from common.models.customer import Customer
from common.models.pay.PayOrderItem import PayOrderItem
from common.models.order import Order
from common.models.address import Address
from common.libs.Helper import getFormatDate
from sqlalchemy import or_
import os
from application import app, db
import time


@route_account.route("/showlog/", methods=['POST'])
def showlog():

    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values

    # page = int(req['page']) if 'page' in req else 1
    # Cid = int(req['Cid']) if 'Cid' in req else 0
    # OrderStatus = int(req['OrderStatus']) if 'OrderStatus' in req else -1
    # info = str(req['mix_kw']) if 'mix_kw' in req else ''
    page = int(req['page']) if 'page' in req else 1
    operating = int(req['operating']) if 'operating' in req else -1
    info = str(req['mix_kw']) if 'mix_kw' in req else ''

    if page < 1:
        page = 1

    page_size = 10
    offset = (page - 1) * page_size
    query = Balancelog.query.filter_by()
    # 待付款：1   申请退款 待付款
    # if OrderStatus == 1:
    #     query = PayOrder.query.filter_by(status=-8)
    # if OrderStatus == 2:
    #     query = PayOrder.query.filter(or_(PayOrder.status == -7, PayOrder.status == -6))
    # if OrderStatus == 3:
    #     query = PayOrder.query.filter(or_(PayOrder.status == 0, PayOrder.status == -5))
    if operating != -1:
        query = Balancelog.query.filter_by(operating=operating)


    if info:
        rule = or_(Balancelog.receipt_qrcode.ilike("%{0}%".format(info)))
        query = query.filter(rule)
        print(query)

    log_list = query.order_by(Balancelog.id.desc()).offset(offset).limit(page_size).all()
    totalCount = query.count()

    data_list = []
    if log_list:
        for item in log_list:
            customer_info = Customer.query.filter_by(Cid=item.Cid).first()
            tmp_data = {
                'receipt_qrcode': item.receipt_qrcode,
                'CustomerName': customer_info.CustomerName,
                'CustomerPhone': customer_info.CustomerPhone,
                'operating': "%s" % (item.operating),
                'balance': str(item.balance),
                'updatetime': str(item.updatetime)
            }
            data_list.append(tmp_data)
    resp['totalCount'] = totalCount
    resp['data'] = data_list
    # resp['data']['has_more'] = 0 if len(data_list) < page_size else 1
    response = jsonify(resp)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@route_account.route("/loginfo/", methods=['POST'])
def loginfo():

    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values

    receipt_qrcode = req['receipt_qrcode'] if 'receipt_qrcode' in req else -1

    loginfo = Balancelog.query.filter_by(receipt_qrcode=receipt_qrcode).first()


    if loginfo:
        customer_info = Customer.query.filter_by(Cid=loginfo.Cid).first()
        tmp_data = {
            'receipt_qrcode': loginfo.receipt_qrcode,
            'CustomerName': customer_info.CustomerName,
            'CustomerPhone': customer_info.CustomerPhone,
            'balance': str(loginfo.balance),
            'status': str(loginfo.status),
            'BankCardNumber': str(loginfo.BankCardNumber),
            'Openingbank': str(loginfo.Openingbank),
            'Accountname': str(loginfo.Accountname),
            'updatetime': str(loginfo.updatetime),
            'operating': "%s" % (loginfo.operating),
        }
        resp['data'] = tmp_data
    response = jsonify(resp)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

# 提现审核
@route_account.route("/auditwithdrawal/", methods=['POST'])
def auditwithdrawal():
    resp = {'code': 200, 'msg': '操作成功'}

    receipt_qrcode = request.values['receipt_qrcode'] if 'receipt_qrcode' in request.values else -1
    status = int(request.values['status']) if 'status' in request.values else -1

    loginfo = Balancelog.query.filter_by(receipt_qrcode=receipt_qrcode).first()
    customer_info = Customer.query.filter_by(Cid=loginfo.Cid).first()

    if status == 1:
        loginfo.freeze_balance = float(0)
        loginfo.status = 3
    elif status == 2:
        freeze_balance = loginfo.freeze_balance
        loginfo.freeze_balance = float(0)
        loginfo.status = 2
        mybalance = float(customer_info.MyBalance)
        result = float(freeze_balance)
        mybalance = mybalance + result
        customer_info.MyBalance = mybalance
    else:
        resp['code'] = -1
        resp['msg'] = '操作失败'
        response = jsonify(resp)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    db.session.commit()
    response = jsonify(resp)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

    # resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    # req = request.values
    #
    # page = int(req['page']) if 'page' in req else 1
    # Shopid = int(req['Shopid']) if 'Shopid' in req else 0
    # OrderStatus = int(req['OrderStatus']) if 'OrderStatus' in req else -1
    # info = str(req['mix_kw']) if 'mix_kw' in req else ''
    #
    # if page < 1:
    #     page = 1
    #
    # page_size = 10
    # offset = (page - 1) * page_size
    # query = Order.query.filter_by()
    #
    # check = [-1, 0]
    # if Shopid not in check and Shopid:
    #     query = Order.query.filter_by(Shopid=Shopid)
    #
    # if OrderStatus != -1 and OrderStatus:
    #     if OrderStatus == 4:
    #         query = Order.query.filter_by(OrderRefundStatus=2)
    #     elif OrderStatus == 5:
    #         query = Order.query.filter_by(OrderRefundStatus=1)
    #     else:
    #         query = Order.query.filter_by(OrderStatus=OrderStatus)
    #
    # if info:
    #     rule = or_(Order.Oid.ilike("%{0}%".format(info)))
    #     query = query.filter(rule)
    #
    # totalCount = query.count()
    #
    # apply_list = query.order_by(Order.Oid.desc()) \
    #     .offset(offset).limit(page_size).all()
    #
    #
    # data_list = []
    # if apply_list:
    #     for item in apply_list:
    #         if item.OrderRefundStatus == 2:
    #             OrderStatus = 4
    #         else:
    #             OrderStatus = item.OrderStatus
    #         tmp_data = {
    #             'Oid': item.Oid,
    #             'Pid': item.Pid,
    #             'Cid': item.Cid,
    #             'Shopid': item.Shopid,
    #             'ProductName': str(item.ProductName),
    #             'OrderCount': str(item.OrderCount),
    #             # 'OrderFormat': str(item.OrderFormat),
    #             'ProductImage': str(item.ProductImage),
    #             'OrderPrice': str(item.OrderPrice),
    #             'OrderTime': str(item.OrderTime),
    #             'OrderStatus': str(OrderStatus),
    #             'OrderRefundStatus': str(item.OrderRefundStatus),
    #             'OrderExpress': str(item.OrderExpress)
    #         }
    #         data_list.append(tmp_data)
    # resp['totalCount'] = totalCount
    # resp['data']['list'] = data_list
    # resp['data']['has_more'] = 0 if len(data_list) < page_size else 1
    # response = jsonify(resp)
    # response.headers['Access-Control-Allow-Origin'] = '*'
    # return response