from web.controllers.account import route_account
from flask import jsonify, request, redirect
from common.models.product import Product
from common.libs.UrlManager import UrlManager
from common.models.shop import Shop
from sqlalchemy import or_
import os
from application import app, db
import time


@route_account.route("/shopedit/")
def shopedit():
    resp = {'code': 200, 'msg': '操作成功~'}
    id = request.values['id'] if 'id' in request.values else -1

    summnerNote = {}

    if id != -1 and id:
        summnerNote = Shop.query.filter_by(id=id).first()
    # else:
    # summnerNote = Shop()

    # summnerNote.Id = request.values['Id'] if 'Id' in request.values else ''
    summnerNote.ShopName = request.values['ShopName'] if 'ShopName' in request.values else ''
    summnerNote.ProductMerchanName = request.values[
        'ProductMerchanName'] if 'ProductMerchanName' in request.values else ''
    summnerNote.ShopInfo = request.values['ShopInfo'] if 'ShopInfo' in request.values else ''
    # summnerNote.ProductInfo = request.values['ProductInfo'] if 'ProductInfo' in request.values else ''

    # try:
    images = request.files['ShopImage']
    for image in images:
        key = str(time.time()).replace('.', '-')
        file_path = os.path.join('Images/', image.filename + key)
        save_path = os.path.join(app.config["ABS_UPLOAD_FOLDER"], image.filename + key)
        image.save(save_path)
        summnerNote.image = file_path
    db.session.add(summnerNote)
    db.session.commit()
    # if id == -1:
    #     id = summnerNote.id
    #     return redirect(UrlManager.buildUrl("/account/edit?id=" + str(id)))
    # else:
    # id = summnerNote.id
    return jsonify(resp)


@route_account.route("/shopadd/")
def shopadd():
    resp = {'code': 200, 'msg': '申请成功，将于三个工作日内进行审核~'}

    # summnerNote = {}

    # if id != -1 and id:
    #     summnerNote = Product.query.filter_by(id=id).first()
    # else:
    summnerNote = Shop()

    # summnerNote.Id = request.values['Id'] if 'Id' in request.values else ''
    summnerNote.ShopName = request.values['ShopName'] if 'ShopName' in request.values else ''
    summnerNote.ProductMerchanName = request.values[
        'ProductMerchanName'] if 'ProductMerchanName' in request.values else ''
    summnerNote.ShopInfo = request.values['ShopInfo'] if 'ShopInfo' in request.values else ''
    # summnerNote.ProductInfo = request.values['ProductInfo'] if 'ProductInfo' in request.values else ''
    # summnerNote.ProdectPrice = request.values['ProdectPrice'] if 'url' in request.values else ''
    # summnerNote.ProductStock = request.values['ProductStock'] if 'ProductStock' in request.values else ''
    summnerNote.ShopStatus = 0
    # try:
    images = request.files['ShopImage']
    for image in images:
        key = str(time.time()).replace('.', '-')
        file_path = os.path.join('Images/', image.filename + request.values['ShopName'] + key)
        save_path = os.path.join(app.config["ABS_UPLOAD_FOLDER"], image.filename + request.values['ShopName'] + key)
        image.save(save_path)
        summnerNote.image = file_path
    db.session.add(summnerNote)
    db.session.commit()
    # if id == -1:
    #     id = summnerNote.id
    #     return redirect(UrlManager.buildUrl("/account/edit?id=" + str(id)))
    # else:
    # id = summnerNote.id
    return jsonify(resp)