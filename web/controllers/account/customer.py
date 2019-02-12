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
                'Cidentity': int(item.Cidentity),
            }
            data_list.append(tmp_data)
    resp['totalCount'] = totalCount
    resp['data']['list'] = data_list
    resp['data']['has_more'] = 0 if len(data_list) < page_size else 1
    response = jsonify(resp)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


# @route_account.route("/shopedit/", methods=['POST'])
# def shopedit():
#
#     resp = {'code': 200, 'msg': '操作成功~'}
#     ShopId = request.values['ShopId'] if 'ShopId' in request.values else -1
#
#     summnerNote = Shop()
#
#     if ShopId != -1 and ShopId:
#         summnerNote = Shop.query.filter_by(ShopId=ShopId).first()
#
#     summnerNote.Aid = request.values['Aid'] if 'Aid' in request.values else ''
#     summnerNote.ShopName = request.values['ShopName'] if 'ShopName' in request.values else ''
#     summnerNote.ShopCategory = request.values['ShopCategory'] if 'ShopCategory' in request.values else ''
#     summnerNote.ShopProvince = request.values['ShopProvince'] if 'ShopProvince' in request.values else ''
#     summnerNote.ShopCity = request.values['ShopCity'] if 'ShopCity' in request.values else ''
#     summnerNote.ShopCountry = request.values['ShopCountry'] if 'ShopCountry' in request.values else ''
#     summnerNote.ShopImage = request.values['ShopImage'] if 'ShopImage' in request.values else ''
#
#     db.session.add(summnerNote)
#     db.session.commit()
#
#     response = jsonify(resp)
#     response.headers['Access-Control-Allow-Origin'] = '*'
#     return response
