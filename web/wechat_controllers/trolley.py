from web.wechat_controllers import route_wechat
from common.models.apply import Apply, db
from application import app, db
from flask import request, jsonify
from common.models.shopping_trolley import ShoppingTrolley
from common.models.order import Order
from common.libs.Helper import getCurrentDate



@route_wechat.route("/showtrolley/", methods=['GET', 'POST'])
def showtrolley():
    resp = {'code': 200, 'msg': '查询成功'}

    Cid = request.values['Cid'] if 'Cid' in request.values else ''

    query = ShoppingTrolley.query.filter_by(Cid=Cid)

    result = query.all()
    tmp_list = []
    for item in result:
        tmp_data = {
            'Id': item.Id,
            'Pid': item.Pid,
            'Cid': item.Cid,
            'Shopid': item.Shopid,
            'ShopName': item.ShopName,
            'ProductName': item.ProductName,
            'ProductImage': item.ProductImage,
            'Count': item.Count,
            'TrolleyPrice': str(item.TrolleyPrice),
            'selected': False
            # 'ProductFormat': item.ProductFormat
        }
        tmp_list.append(tmp_data)

    resp['list'] = tmp_list

    return jsonify(resp)

@route_wechat.route("/addtrolley/", methods=['GET', 'POST'])
def addtrolley():
    resp = {'code': 200, 'msg': '添加成功'}

    summnerNote = ShoppingTrolley()

    summnerNote.Pid = request.values['Pid'] if 'Pid' in request.values else ''
    summnerNote.Cid = request.values['Cid'] if 'Cid' in request.values else ''
    summnerNote.Shopid = request.values['Shopid'] if 'Shopid' in request.values else ''
    summnerNote.ShopName = request.values['ShopName'] if 'ShopName' in request.values else ''
    summnerNote.ProductName = request.values['ProductName'] if 'ProductName' in request.values else ''
    summnerNote.ProductImage = request.values['ProductImage'] if 'ProductImage' in request.values else ''
    summnerNote.Count = request.values['Count'] if 'Count' in request.values else ''
    summnerNote.TrolleyPrice = request.values['TrolleyPrice'] if 'TrolleyPrice' in request.values else ''
    # summnerNote.ProductFormat = request.values['ProductFormat'] if 'ProductFormat' in request.values else ''

    db.session.add(summnerNote)
    db.session.commit()

    return jsonify(resp)

@route_wechat.route("/trolleyorder/", methods=['GET', 'POST'])
def trolleyorder():
    resp = {'code': 200, 'msg': '下单成功'}

    summnerNote = Order()

    summnerNote.Pid = request.values['Pid'] if 'Pid' in request.values else ''
    summnerNote.Cid = request.values['Cid'] if 'Cid' in request.values else ''
    summnerNote.Shopid = request.values['Shopid'] if 'Shopid' in request.values else -1
    summnerNote.ProductName = request.values['ProductName'] if 'ProductName' in request.values else ''
    summnerNote.OrderCount = request.values['OrderCount'] if 'OrderCount' in request.values else ''
    # summnerNote.OrderFormat = request.values['OrderFormat'] if 'OrderFormat' in request.values else ''
    summnerNote.ProductImage = request.values['ProductImage'] if 'ProductImage' in request.values else ''
    price = request.values['OrderPrice'] if 'OrderPrice' in request.values else 0
    summnerNote.OrderPrice = float('%.2f' % (float(price) * int(summnerNote.OrderCount)))
    summnerNote.OrderAddress = request.values['OrderAddress'] if 'OrderAddress' in request.values else ''
    summnerNote.OrderRefund = ''
    summnerNote.OrderExpress = -1
    summnerNote.OrderTime = getCurrentDate()
    summnerNote.OrderStatus = 1
    summnerNote.OrderRefundStatus = 0

    db.session.add(summnerNote)
    db.session.commit()

    return jsonify(resp)

@route_wechat.route("/deletetrolley/", methods=['GET', 'POST'])
def deletetrolley():
    resp = {'code': 200, 'msg': '删除成功'}

    Id = request.values['Id'] if 'Id' in request.values else -1

    result = ShoppingTrolley.query.filter_by(Id=Id).first()
    db.session.delete(result)
    db.session.commit()
    return jsonify(resp)