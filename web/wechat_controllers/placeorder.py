from web.wechat_controllers import route_wechat
from application import app, db
from flask import request, jsonify
from sqlalchemy import or_
from common.models.order import Order
from common.models.shopping_trolley import ShoppingTrolley
from common.models.address import Address
from common.libs.pay.wechatService import WeChatService
from common.libs.Helper import getCurrentDate, getFormatDate
import json


@route_wechat.route("/placeorder/", methods=['POST'])
def placeorder():
    resp = {'code': 200, 'msg': '下单成功'}
    trolley_result = request.values['trolley_list']
    if trolley_result:
        trolley_list = trolley_result.strip(',').split(',')
        if trolley_list:
            for item in trolley_list:
                result = ShoppingTrolley.query.filter_by(Id=int(item)).first()
                db.session.delete(result)
                db.session.commit()

    result = json.loads(request.values['order_list'])
    for item in result:
        summnerNote = Order()
        summnerNote.Pid = item['Pid'] if 'Pid' in item else ''
        summnerNote.Cid = item['Cid'] if 'Cid' in item else ''
        summnerNote.Shopid = item['Shopid'] if 'Shopid' in item else -1
        summnerNote.ProductName = item['ProductName'] if 'ProductName' in item else ''
        summnerNote.OrderCount = item['OrderCount'] if 'OrderCount' in item else ''
        # summnerNote.OrderFormat = request.values['OrderFormat'] if 'OrderFormat' in request.values else ''
        summnerNote.ProductImage = item['ProductImage'] if 'ProductImage' in item else ''
        price = item['OrderPrice'] if 'OrderPrice' in item else 0
        summnerNote.OrderPrice = float('%.2f' % (float(price) * int(summnerNote.OrderCount)))
        summnerNote.OrderAddress = item['OrderAddress'] if 'OrderAddress' in item else ''
        summnerNote.OrderRefund = ''
        summnerNote.OrderExpress = -1
        summnerNote.OrderTime = getCurrentDate()
        summnerNote.OrderStatus = 1
        summnerNote.OrderRefundStatus = 0

        db.session.add(summnerNote)
        db.session.commit()

    return jsonify(resp)


@route_wechat.route("/showorder/", methods=['POST'])
def showorder():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values

    Cid = int(req['Cid']) if 'Cid' in req else -1
    page = int(req['page']) if 'page' in req else 1
    OrderStatus = int(req['OrderStatus']) if 'OrderStatus' in req else -1

    if page < 1:
        page = 1

    page_size = 5
    offset = (page - 1) * page_size
    if Cid:
        query = Order.query.filter_by(Cid=Cid)
    # 待付款：1   申请退款 待付款
    if OrderStatus == 1:
        query = Order.query.filter_by(OrderStatus=1)
    if OrderStatus == 2:
        query = Order.query.filter(or_(Order.OrderStatus == 2, Order.OrderStatus == 6))
    if OrderStatus == 3:
        query = Order.query.filter(or_(Order.OrderStatus == 3, Order.OrderStatus == 5, Order.OrderStatus == 7))

    totalCount = query.count()

    apply_list = query.order_by(Order.Cid.desc()) \
        .offset(offset).limit(page_size).all()

    data_list = []
    if apply_list:
        for item in apply_list:
            # if item.OrderRefundStatus == 2:
            #     OrderStatus = 4
            # else:
            #     OrderStatus = item.OrderStatus
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
                'OrderStatus': str(item.OrderStatus),
                'OrderExpress': str(item.OrderExpress),
                'OrderRefundStatus': str(item.OrderRefundStatus)
            }
            data_list.append(tmp_data)
    resp['totalCount'] = totalCount
    resp['data']['list'] = data_list
    resp['data']['has_more'] = 0 if len(data_list) < page_size else 1
    response = jsonify(resp)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@route_wechat.route("/orderinfo/", methods=['POST'])
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
            'OrderStatus': int(OrderInfo.OrderStatus),
            'OrderAddressInfo': address
        }
        resp['data'] = tmp_data
    return jsonify(resp)

@route_wechat.route("/orderRefund/", methods=['POST'])
def orderRefund():
    resp = {'code': 200, 'msg': '申请成功，1~3个工作日内进行审核！'}
    req = request.values

    Oid = int(req['Oid']) if 'Oid' in req else -1
    OrderRefund = req['OrderRefund'] if 'OrderRefund' in req else -1
    OrderRefundStatus = 2

    result = Order.query.filter_by(Oid=Oid).first()
    result.OrderRefundStatus = int(OrderRefundStatus)
    result.OrderExpress = str(OrderRefund)

    db.session.commit()
    response = jsonify(resp)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@route_wechat.route("/deleteorder/", methods=['GET', 'POST'])
def deleteorder():
    resp = {'code': 200, 'msg': '取消成功'}

    Oid = request.values['Oid'] if 'Oid' in request.values else -1
    result = Order.query.filter_by(Oid=Oid).first()
    result.OrderStatus = 7

    db.session.commit()
    return jsonify(resp)
