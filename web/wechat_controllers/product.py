from web.wechat_controllers import route_wechat
from common.models.apply import Apply, db
from application import app, db
from flask import request, jsonify
from common.models.order import Order
from common.libs.Helper import getCurrentDate


@route_wechat.route("/productinfo/", methods=['GET', 'POST'])
def productinfo():
    resp = {'code': 200, 'msg': '下单成功'}

    summnerNote = Order()

    summnerNote.Pid = request.values['Pid'] if 'Pid' in request.values else ''
    summnerNote.Cid = request.values['Cid'] if 'Cid' in request.values else ''
    summnerNote.ProductName = request.values['ProductName'] if 'ProductName' in request.values else ''
    summnerNote.ProductImage = request.values['ProductImage'] if 'ProductImage' in request.values else ''
    summnerNote.ProdectPrice = request.values['ProdectPrice'] if 'ProdectPrice' in request.values else ''
    summnerNote.OrderTime = getCurrentDate()
    summnerNote.OrderStatus = 0

    db.session.add(summnerNote)
    db.session.commit()

    return jsonify(resp)

@route_wechat.route("/showorder/", methods=['GET', 'POST'])
def customerinfo():

    resp = {'code': 200, 'msg': '查询成功'}
    req = request.values
    Cid = req['Cid']
    orders = Order.query.filter_by(Cid=Cid).all
    order_list = []
    for order in orders:
        result = {
            'Cid': Cid,
            'CustomerName': order.CustomerName,
            'CustomerPhone': order.CustomerPhone,
            'MyBalance': str(order.MyBalance),
            'AvailableBalance': order.AvailableBalance,
            "MyIncome": order.MyIncome
        }
        order_list.append(result)
    resp['order_list'] = order_list
    return jsonify(resp)





