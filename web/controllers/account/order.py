from web.controllers.account import route_account
from flask import jsonify, request, redirect
from common.models.product import Product
from common.libs.UrlManager import UrlManager
from common.models.pay.PayOrder import PayOrder
from common.models.pay.PayOrderItem import PayOrderItem
from common.models.Balacelog.Balancelog import Balancelog
from common.models.shop import Shop
from common.models.address import Address
from common.models.apply import Apply
from common.models.customer import Customer
from common.libs.Helper import getCurrentDate
from common.libs.Helper import getFormatDate
from sqlalchemy import or_
from common.libs.pay.PayService import PayService
import os
from application import app, db
import time


@route_account.route("/showorder/", methods=['POST'])
def showorder():

    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values

    # page = int(req['page']) if 'page' in req else 1
    # Shopid = int(req['Shopid']) if 'Shopid' in req else 0
    # OrderStatus = int(req['OrderStatus']) if 'OrderStatus' in req else -1
    # info = str(req['mix_kw']) if 'mix_kw' in req else ''

    Shopid = int(req['Shopid']) if 'Shopid' in req else -1
    page = int(req['page']) if 'page' in req else 1
    OrderStatus = int(req['OrderStatus']) if 'OrderStatus' in req else -1
    info = str(req['mix_kw']) if 'mix_kw' in req else ''

    if page < 1:
        page = 1

    page_size = 10
    offset = (page - 1) * page_size
    if Shopid and Shopid != 0:
        query = PayOrder.query.filter_by(Shopid=Shopid)
    else:
        query = PayOrder.query
    # 待付款：1   申请退款 待付款
    # if OrderStatus == 1:
    #     query = PayOrder.query.filter_by(status=-8)
    # if OrderStatus == 2:
    #     query = PayOrder.query.filter(or_(PayOrder.status == -7, PayOrder.status == -6))
    # if OrderStatus == 3:
    #     query = PayOrder.query.filter(or_(PayOrder.status == 0, PayOrder.status == -5))
    if OrderStatus != -1:
        query = PayOrder.query.filter_by(status=OrderStatus)

    totalCount = query.count()

    if info:
        rule = or_(PayOrder.id.ilike("%{0}%".format(info)))
        query = query.filter(rule)

    order_list = query.order_by(PayOrder.id.desc()).offset(offset).limit(page_size).all()

    o_list = []
    if order_list:
        for item in order_list:
            pay_order_item_query = PayOrderItem.query.filter_by(pay_order_id=int(item.id))
            pay_order_item = pay_order_item_query.order_by(PayOrderItem.id.desc()).all()
            data_list = []
            for info in pay_order_item:
                Product_info = Product.query.filter_by(Pid=info.Pid).first()
                # data_list['OrderStatus'] = item.status
                tmp_data = {
                    'id': item.id,   # 订单id
                    'Pid': info.Pid,
                    'Cid': item.member_id,
                    'order_sn': item.order_sn,
                    'Shopid': Product_info.Shopid,
                    'ProductName': str(Product_info.ProductName),
                    'OrderCount': str(info.quantity),
                    # 'OrderFormat': str(item.OrderFormat),
                    'ProductImage': str(Product_info.ProductImage),
                    'OrderPrice': str(info.price),
                    'OrderTime': str(item.updated_time),
                    'OrderStatus': str(item.status)
                    # 'OrderExpress': str(item.OrderExpress)
                }
                data_list.append(tmp_data)
            o_list.append(data_list)
    resp['totalCount'] = totalCount
    resp['data']['list'] = o_list
    resp['data']['has_more'] = 0 if len(o_list) < page_size else 1
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

@route_account.route("/orderinfo/", methods=['POST'])
def orderinfo():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}, 'OrderAddressInfo': {}, 'pay_price': {}}
    req = request.values

    id = int(req['id']) if 'id' in req else -1

    Pay_info = PayOrder.query.filter_by(id=id).first()
    OrderInfo = PayOrderItem.query.filter_by(pay_order_id=id).all()


    if OrderInfo:
        AddressInfo = Pay_info.express_address_id
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
        data_list = []
        for item in OrderInfo:
            ProductInfo = Product.query.filter_by(Pid=item.Pid).first()
            tmp_data = {
                'Oid': item.pay_order_id,
                'Pid': item.Pid,
                'Shopid': ProductInfo.Shopid,
                'ProductName': "%s" % (ProductInfo.ProductName),
                'OrderCount': "%s" % (item.quantity),
                'ProductImage': "%s" % (ProductInfo.ProductImage),
                'OrderPrice': "%s" % (item.price),
                'OrderTime': getFormatDate(item.updated_time),
                'tracking_number': "%s" % (Pay_info.tracking_number),
                'OrderStatus': int(Pay_info.status)
                # 'OrderAddressInfo': address
            }
            data_list.append(tmp_data)
        resp['data'] = data_list
        resp['OrderAddressInfo'] = address
        resp['pay_price'] = str(Pay_info.pay_price)
    response = jsonify(resp)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
    #  resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    # req = request.values
    #
    # Oid = int(req['Oid']) if 'Oid' in req else -1
    #
    # OrderInfo = Order.query.filter_by(Oid=Oid).first()
    #
    #
    # if OrderInfo:
    #     AddressInfo = OrderInfo.OrderAddress
    #     AddressInfo = Address.query.filter_by(Id=AddressInfo).first()
    #
    #     address = {
    #         'id': AddressInfo.Id,
    #         'Cid': AddressInfo.Cid,
    #         'Addressee': AddressInfo.Addressee,
    #         'AddresseePhone': AddressInfo.AddresseePhone,
    #         'Province': AddressInfo.Province,
    #         'City': AddressInfo.City,
    #         'County': AddressInfo.County,
    #         'Details': AddressInfo.Details,
    #         'Status': int(AddressInfo.Status)
    #     }
    #     # if OrderInfo.OrderRefundStatus == 2:
    #     #     OrderStatus = 4
    #     # else:
    #     OrderStatus = OrderInfo.OrderStatus
    #     tmp_data = {
    #         'Oid': OrderInfo.Oid,
    #         'Pid': OrderInfo.Oid,
    #         'Cid': OrderInfo.Cid,
    #         'Shopid': OrderInfo.Shopid,
    #         'ProductName': "%s" % (OrderInfo.ProductName),
    #         'OrderCount': "%s" % (OrderInfo.OrderCount),
    #         'ProductImage': "%s" % (OrderInfo.ProductImage),
    #         'OrderPrice': "%s" % (OrderInfo.OrderPrice),
    #         'OrderTime': getFormatDate(OrderInfo.OrderTime),
    #         'OrderRefund': OrderInfo.OrderRefund,
    #         'OrderRefundStatus': OrderInfo.OrderRefundStatus,
    #         'OrderStatus': int(OrderStatus),
    #         'OrderAddressInfo': address
    #     }
    #     resp['data'] = tmp_data
    # response = jsonify(resp)
    # response.headers['Access-Control-Allow-Origin'] = '*'
    # return response

# 退款审核
@route_account.route("/order_refund/", methods=['POST'])
def order_refund():
    # resp = {'code': 200, 'msg': '操作成功'}
    # Oid = request.values['Oid'] if 'Oid' in request.values else -1
    # OrderStatus = request.values['OrderStatus'] if 'OrderStatus' in request.values else 0
    # OrderRefundStatus = request.values['OrderRefundStatus'] if 'OrderRefundStatus' in request.values else 0
    # result = Order.query.filter_by(Oid=Oid).first()
    # result.OrderRefundStatus = int(OrderRefundStatus)
    # result.OrderStatus = int(OrderStatus)
    #
    # db.session.commit()

    resp = {'code': 200, 'msg': '取消成功'}

    id = request.values['id'] if 'id' in request.values else -1
    result = PayOrder.query.filter_by(id=id).first()
    result.status = 0

    # 返回库存
    pay_order_item_info = PayOrderItem.query.filter_by(pay_order_id=result.id).all()
    for item in pay_order_item_info:
        product_info = Product.query.filter_by(Pid=item.Pid).first()
        stock = int(product_info.ProductStock)
        stock_result = stock + int(item.quantity)
        product_info.ProductStock = stock_result

    db.session.commit()
    response = jsonify(resp)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@route_account.route("/ordersend/", methods=['POST'])
def ordersend():
    # resp = {'code': 200, 'msg': '操作成功'}
    # Oid = request.values['Oid'] if 'Oid' in request.values else -1
    # OrderStatus = request.values['OrderStatus'] if 'OrderStatus' in request.values else 0
    # OrderRefundStatus = request.values['OrderRefundStatus'] if 'OrderRefundStatus' in request.values else 0
    # result = Order.query.filter_by(Oid=Oid).first()
    # result.OrderRefundStatus = int(OrderRefundStatus)
    # result.OrderStatus = int(OrderStatus)
    #
    # db.session.commit()

    resp = {'code': 200, 'msg': '发货成功'}

    id = request.values['id'] if 'id' in request.values else -1
    tracking_number = request.values['tracking_number'] if 'tracking_number' in request.values else -1
    result = PayOrder.query.filter_by(id=id).first()
    result.status = -6
    result.tracking_number = tracking_number

    db.session.commit()
    response = jsonify(resp)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@route_account.route("/confirmreceipt/", methods=['POST'])
def confirmreceipt():

    # 确认收货
    # 增加销量
    # 用户冻结金额清零
    # 商户余额增加加入记录

    resp = {'code': 200, 'msg': '确认收货成功'}

    Oid = request.values['Oid'] if 'Oid' in request.values else -1
    Shopid = request.values['Shopid'] if 'Shopid' in request.values else -1

    Pay_info = PayOrder.query.filter_by(id=Oid).first()
    Pay_info.status = -5
    loginfo = Balancelog.query.filter_by(receipt_qrcode=Pay_info.order_sn).first()
    Shop_info = Shop.query.filter_by(Shopid=Shopid).first()
    Apply_info = Apply.query.filter_by(Aid=Shop_info.Aid).first()
    # 商户Cid
    Customer_info = Customer.query.filter_by(Cid=Apply_info.Cid).first()

    # 用户冻结金额清零
    freeze_balance = loginfo.freeze_balance
    loginfo.freeze_balance = float(0)

    mybalance = float(Customer_info.MyBalance)
    result = float(freeze_balance)
    mybalance = mybalance + result
    Customer_info.MyBalance = mybalance

    # 销量增加
    pay_order_item_info = PayOrderItem.query.filter_by(pay_order_id=Pay_info.id).all()
    for item in pay_order_item_info:
        product_info = Product.query.filter_by(Pid=item.Pid).first()
        sold = int(product_info.ProductSold)
        sold_result = sold + item.quantity
        product_info.ProductSold = sold_result

    # 打款给商家记录
    Balance_log = Balancelog()

    Balance_log.BankCardNumber = -1000
    Balance_log.Cid = Customer_info.Cid
    Balance_log.Openingbank = -1000
    Balance_log.balance = freeze_balance
    Balance_log.operating = 4
    Balance_log.status = 6
    Balance_log.total_balance = freeze_balance
    target_pay = PayService()
    Balance_log.receipt_qrcode = target_pay.geneOrderSn()
    Balancelog.freeze_balance = float(0)
    Balance_log.Accountname = -1000
    Balance_log.createtime = getCurrentDate()
    Balance_log.updatetime = getCurrentDate()
    db.session.add(Balance_log)

    db.session.commit()
    response = jsonify(resp)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response