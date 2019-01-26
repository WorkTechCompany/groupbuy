from web.controllers.account import route_account
from flask import jsonify, request
from common.models.product import Product
from common.libs.UrlManager import UrlManager
from sqlalchemy import or_
import os
from application import app, db
import time


@route_account.route("/allproduct/")
def allproduct():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values

    info = str(req['mix_kw']) if 'mix_kw' in req else ''
    page = int(req['page']) if 'page' in req else 1
    ProductMerchantId = int(req['ProductMerchantId']) if 'page' in req else 0

    if page < 1:
        page = 1

    page_size = 10
    offset = (page - 1) * page_size
    query = Product.query.filter_by(ProductMerchantId=ProductMerchantId)

    if info:
        rule = or_(Product.ShopName.ilike("%{0}%".format(info)))
        query = query.filter(rule)

    shop_list = query.order_by(Product.Id.desc()) \
        .offset(offset).limit(page_size).all()

    data_food_list = []
    if shop_list:
        for item in shop_list:
            tmp_data = {
                'id': item.Id,
                'ProductName': "%s" % (item.ProductName),
                'ProductMerchantId': "%s" % (item.ProductMerchantId),
                'ProductCategory': str(item.ProductCategory),
                'ProdectPrice': str(item.ProdectPrice),
                'ProductImage': str(item.ProductImage),
                'ProductStock': int(item.ProductStock),
                'ProductSold': str(item.ProductSold),
                'ProductStatus': str(item.ProductStatus)
            }
            data_food_list.append(tmp_data)
    resp['data']['list'] = data_food_list
    resp['data']['has_more'] = 0 if len(data_food_list) < page_size else 1

    return jsonify(resp)


@route_account.route('/productedit', methods=['GET', 'POST'])
def productedit():
    resp = {'code': 200, 'msg': '操作成功~'}
    id = request.values['id'] if 'id' in request.values else -1

    summnerNote = {}

    if id != -1 and id:
        summnerNote = Product.query.filter_by(id=id).first()
    # else:
    # summnerNote = Product()

    # summnerNote.Id = request.values['Id'] if 'Id' in request.values else ''
    summnerNote.ProductName = request.values['ProductName'] if 'ProductName' in request.values else ''
    summnerNote.ProductMerchanName = request.values[
        'ProductMerchanName'] if 'ProductMerchanName' in request.values else ''
    summnerNote.ProductCategory = request.values['ProductCategory'] if 'ProductCategory' in request.values else ''
    summnerNote.ProductInfo = request.values['ProductInfo'] if 'ProductInfo' in request.values else ''
    summnerNote.ProdectPrice = request.values['ProdectPrice'] if 'url' in request.values else ''
    summnerNote.ProductStock = request.values['ProductStock'] if 'ProductStock' in request.values else ''
    summnerNote.ProductStatus = 0

    # try:
    images = request.files['ProductImage']
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
    # except:
    #     db.session.add(summnerNote)
    #     db.session.commit()
    #     if id == -1:
    #         id = summnerNote.id
    #         return redirect(UrlManager.buildUrl("/account/edit?id=" + str(id)))
    #     else:
    #         id = summnerNote.id
    #         return redirect(UrlManager.buildUrl("/account/edit?id=" + str(id)))


@route_account.route('/addproduct', methods=['GET', 'POST'])
def addproduct():
    resp = {'code': 200, 'msg': '添加成功~'}

    summnerNote = {}

    # if id != -1 and id:
    #     summnerNote = Product.query.filter_by(id=id).first()
    # else:
    summnerNote = Product()

    summnerNote.ProductName = request.values['ProductName'] if 'ProductName' in request.values else ''
    summnerNote.ProductMerchanName = request.values[
        'ProductMerchanName'] if 'ProductMerchanName' in request.values else ''
    summnerNote.ProductCategory = request.values['ProductCategory'] if 'ProductCategory' in request.values else ''
    summnerNote.ProductInfo = request.values['ProductInfo'] if 'ProductInfo' in request.values else ''
    summnerNote.ProdectPrice = request.values['ProdectPrice'] if 'url' in request.values else ''
    summnerNote.ProductStock = request.values['ProductStock'] if 'ProductStock' in request.values else ''
    summnerNote.ProductStatus = 0

    # try:
    images = request.files['ProductImage']
    for key, image in enumerate(images):
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

@route_account.route('/deleteproduct', methods=['GET', 'POST'])
def deleteproduct():
    resp = {'code': 200, 'msg': '删除成功'}

    id = request.values['id'] if 'id' in request.values else -1

    result = Product.query.filter_by(id=id).first()
    db.session.delete(result)
    db.session.commit()
    return jsonify(resp)



@route_account.route('/upload_img/', methods=['GET', 'POST'])
def upload_img():
    response = {'status': 1, 'message': '文件上传成功'}
    image = request.files['file']
    file_path = os.path.join('Images/', image.filename)
    save_path = os.path.join(app.config["ABS_UPLOAD_FOLDER"], image.filename)
    image.save(save_path)
    result = UrlManager.buildImageUrl(file_path)
    response['img'] = result
    return jsonify(response)
