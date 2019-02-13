from web.controllers.account import route_account
from flask import jsonify, request
from common.models.apply import Apply
from common.models.customer import Customer
from common.libs.UrlManager import UrlManager
from sqlalchemy import or_
import os
from application import app, db
import time

# 商户申请显示
@route_account.route("/showapply/", methods=['POST'])
def showapply():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values

    page = int(req['page']) if 'page' in req else 1
    ApplyStatus = int(req['ApplyStatus']) if 'ApplyStatus' in req else 2

    if page < 1:
        page = 1

    page_size = 10
    offset = (page - 1) * page_size
    if ApplyStatus == 2:
        query = Apply.query.filter_by()
    else:
        query = Apply.query.filter_by(ApplyStatus=ApplyStatus)

    totalCount = query.count()

    apply_list = query.order_by(Apply.Aid.desc()) \
        .offset(offset).limit(page_size).all()

    data_list = []
    if apply_list:
        for item in apply_list:
            tmp_data = {
                'Aid': item.Aid,
                'ShopCategory': str(item.ShopCategory),
                'IdentityCard': str(item.IdentityCard),
                'IdentityCardHand': str(item.IdentityCardHand),
                'BusinessLicense': str(item.BusinessLicense),
                'Contract': str(item.Contract),
                'IDCard': str(item.IDCard),
                'ApplyProvince': str(item.ApplyProvince),
                'ApplyCity': str(item.ApplyCity),
                'ApplyCounty': str(item.ApplyCounty),
                'ApplyDetails': str(item.ApplyDetails),
                'ApplyPhone': str(item.ApplyPhone),
                'ApplyPassword': str(item.ApplyPassword),
                'ApplyStatus': int(item.ApplyStatus),
            }
            data_list.append(tmp_data)
    resp['totalCount'] = totalCount
    resp['data']['list'] = data_list
    resp['data']['has_more'] = 0 if len(data_list) < page_size else 1
    response = jsonify(resp)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

# 商户申请审核
@route_account.route("/changestatus/", methods=['POST'])
def changestatus():
    resp = {'code': 200, 'msg': '操作成功'}

    Aid = request.values['Aid'] if 'Aid' in request.values else -1
    ApplyStatus = request.values['ApplyStatus'] if 'ApplyStatus' in request.values else 0
    result = Apply.query.filter_by(Aid=Aid).first()
    result.ApplyStatus = int(ApplyStatus)

    Cid = result.Cid
    result = Customer.query.filter_by(Cid=Cid).first()
    result.Cidentity = 2

    db.session.commit()
    response = jsonify(resp)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


# 商户申请删除
@route_account.route('/deleteapply/', methods=['GET', 'POST'])
def edditstatus():
    resp = {'code': 200, 'msg': '操作成功'}

    Aid = request.values['Aid'] if 'Aid' in request.values else -1

    result = Apply.query.filter_by(Aid=Aid).first()
    db.session.delete(result)
    db.session.commit()
    return jsonify(resp)

