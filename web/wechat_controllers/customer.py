from web.wechat_controllers import route_wechat
from common.models.apply import Apply, db
from application import app, db
from flask import request, jsonify
from common.models.customer import Customer


# 用户信息
# 注册
@route_wechat.route("/customeSignin/", methods=['GET', 'POST'])
def customesignin():

    return '注册成功'


# 用户余额
@route_wechat.route("/CustomerInfo/", methods=['GET', 'POST'])
def customerinfo():

    resp = {'code': 200, 'msg': '查询成功'}
    req = request.values
    Cid = req['Cid']
    info = Customer.query.filter_by(Cid=Cid).first()
    resp['info'] = {
        'Cid': Cid,
        'CustomerName': info.CustomerName,
        'CustomerPhone': info.CustomerPhone,
        'MyBalance': str(info.MyBalance),
        'AvailableBalance': info.AvailableBalance,
        "MyIncome": info.MyIncome
    }
    return jsonify(resp)





