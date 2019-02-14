from web.controllers.account import route_account
from flask import jsonify, request, redirect
from common.models.product import Product
from common.libs.UrlManager import UrlManager
from common.models.customer import Customer
from sqlalchemy import or_
import os
from application import app, db
import time


@route_account.route("/showcustomer/", methods=['POST'])
def showcustomer():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values

    page = int(req['page']) if 'page' in req else 1
    Cidentity = int(req['Cidentity']) if 'Cidentity' in req else -1
    info = str(req['mix_kw']) if 'mix_kw' in req else ''

    if page < 1:
        page = 1

    page_size = 10
    offset = (page - 1) * page_size
    query = Customer.query.filter_by()
    if Cidentity != -1 and Cidentity:
        query = Customer.query.filter_by(Cidentity=Cidentity)

    if info:
        rule = or_(Customer.CustomerName.ilike("%{0}%".format(info)), Customer.CustomerPhone.ilike("%{0}%".format(info)))
        query = query.filter(rule)

    totalCount = query.count()

    apply_list = query.order_by(Customer.Cid.desc()) \
        .offset(offset).limit(page_size).all()

    data_list = []
    if apply_list:
        for item in apply_list:
            tmp_data = {
                'Cid': item.Cid,
                'CustomerName': str(item.CustomerName),
                'CustomerPhone': str(item.CustomerPhone),
                'MyBalance': str(item.MyBalance),
                'AvailableBalance': str(item.AvailableBalance),
                'MyIncome': str(item.MyIncome),
                'Cidentity': int(item.Cidentity),
            }
            data_list.append(tmp_data)
    resp['totalCount'] = totalCount
    resp['data']['list'] = data_list
    resp['data']['has_more'] = 0 if len(data_list) < page_size else 1
    response = jsonify(resp)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

