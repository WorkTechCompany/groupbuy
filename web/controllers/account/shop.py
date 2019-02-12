from web.controllers.account import route_account
from flask import jsonify, request, redirect
from common.models.product import Product
from common.libs.UrlManager import UrlManager
from common.models.shop import Shop
from sqlalchemy import or_
import os
from application import app, db
import time


@route_account.route("/getshopinfo/")
def getshopinfo():
    resp = {'code': 200, 'msg': '查询成功~'}
    Aid = request.values['Aid'] if 'Aid' in request.values else -1
    result = Shop.query.filter_by(Aid=Aid).first()

    if result:
        tmp_data = {
            'ShopId': result.ShopId,
            'Aid': result.Aid,
            'ShopName': str(result.ShopName),
            'ShopImage': str(result.ShopImage),
            'ShopCategory': int(result.ShopCategory),
            'ShopProvince': str(result.ShopProvince),
            'ShopCity': str(result.ShopCity),
            'ShopCountry': str(result.ShopCountry)
        }
        resp['info'] = tmp_data
        response = jsonify(resp)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    resp['msg'] = '请添加店铺信息'
    resp['code'] = 205
    response = jsonify(resp)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@route_account.route("/shopedit/", methods=['POST'])
def shopedit():

    resp = {'code': 200, 'msg': '操作成功~'}
    ShopId = request.values['ShopId'] if 'ShopId' in request.values else -1

    summnerNote = Shop()

    if ShopId != -1 and ShopId:
        summnerNote = Shop.query.filter_by(ShopId=ShopId).first()

    summnerNote.Aid = request.values['Aid'] if 'Aid' in request.values else ''
    summnerNote.ShopName = request.values['ShopName'] if 'ShopName' in request.values else ''
    summnerNote.ShopCategory = request.values['ShopCategory'] if 'ShopCategory' in request.values else ''
    summnerNote.ShopProvince = request.values['ShopProvince'] if 'ShopProvince' in request.values else ''
    summnerNote.ShopCity = request.values['ShopCity'] if 'ShopCity' in request.values else ''
    summnerNote.ShopCountry = request.values['ShopCountry'] if 'ShopCountry' in request.values else ''
    summnerNote.ShopImage = request.values['ShopImage'] if 'ShopImage' in request.values else ''

    db.session.add(summnerNote)
    db.session.commit()

    response = jsonify(resp)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
