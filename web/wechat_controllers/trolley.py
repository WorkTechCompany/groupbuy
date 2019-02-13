from web.wechat_controllers import route_wechat
from common.models.apply import Apply, db
from application import app, db
from flask import request, jsonify
from common.models.shopping_trolley import ShoppingTrolley
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
            'ShopId': item.ShopId,
            'ShopName': item.ShopName,
            'ProductName': item.ProductName,
            'Count': item.Count,
            'ProdectPrice': item.ProdectPrice,
            'ProductFormat': item.ProductFormat
        }
        tmp_list.append(tmp_data)

    resp['list'] = tmp_list

    return jsonify(resp)

@route_wechat.route("/addtrolley/", methods=['GET', 'POST'])
def addtrolley():
    resp = {'code': 200, 'msg': '添加成功'}

    summnerNote = ShoppingTrolley()

    summnerNote.Cid = request.values['Cid'] if 'Cid' in request.values else ''
    summnerNote.ShopId = request.values['ShopId'] if 'ShopId' in request.values else ''
    summnerNote.ShopName = request.values['ShopName'] if 'ShopName' in request.values else ''
    summnerNote.ProductName = request.values['ProductName'] if 'ProductName' in request.values else ''
    summnerNote.Count = request.values['Count'] if 'Count' in request.values else ''
    summnerNote.ProductPrice = request.values['ProdectPrice'] if 'ProdectPrice' in request.values else ''
    summnerNote.ProductFormat = request.values['ProductFormat'] if 'ProductFormat' in request.values else ''

    db.session.add(summnerNote)
    db.session.commit()

    return jsonify(resp)
