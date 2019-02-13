from web.controllers.account import route_account
from flask import jsonify, request
from common.models.product import Product
from common.libs.UrlManager import UrlManager
from common.models.productimage import Productimage
from common.models.productformat import ProductFormat
from sqlalchemy import or_
import os
from application import app, db
import time
import json, decimal

# 所有商品
@route_account.route("/allproduct/", methods=['POST'])
def allproduct():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values

    category = int(req['cat']) if 'cat' in req else ''
    info = str(req['mix_kw']) if 'mix_kw' in req else ''
    page = int(req['page']) if 'page' in req else 1
    # ShopId = int(req['ProductMerchantId']) if 'page' in req else 0

    if page < 1:
        page = 1

    page_size = 10
    offset = (page - 1) * page_size
    query = Product.query.filter_by()

    if info:
        rule = or_(Product.ProductName.ilike("%{0}%".format(info)))
        query = query.filter(rule)

    if category:
        query = query.filter_by(ProductCategory=category)

    totalCount = query.count()

    shop_list = query.order_by(Product.PId.desc()).offset(offset).limit(page_size).all()

    data_food_list = []
    if shop_list:
        for item in shop_list:
            image = json.loads(item.ProductImage)

            tmp_data = {
                'PId': item.PId,
                'ProductName': "%s" % (item.ProductName),
                'ShopId': "%s" % (item.ShopId),
                'ProductCategory': str(item.ProductCategory),
                'ProductImage': str(image[0]),
                'ProductFormat': str(item.ProductFormat),
                'ProductSold': str(item.ProductSold),
            }
            data_food_list.append(tmp_data)
    resp['data']['list'] = data_food_list
    resp['data']['has_more'] = 0 if len(data_food_list) < page_size else 1
    resp['totalCount'] = totalCount

    response = jsonify(resp)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

# 编辑商品
@route_account.route('/productedit/', methods=['GET', 'POST'])
def productedit():
    resp = {'code': 200, 'msg': '操作成功~'}
    PId = request.values['PId'] if 'PId' in request.values else -1
    if request.method == 'GET':
        result = Product.query.filter_by(PId=PId).first()

        if result:
            tmp_data = {
                'PId': result.PId,
                'ProductName': "%s" % (result.ProductName),
                'ShopId': "%s" % (result.ShopId),
                'ProductCategory': str(result.ProductCategory),
                'ProductImage': str(result.ProductImage),
                'Productsku': str(result.Productsku),
                'ProductFormat': str(result.ProductFormat),
                'ProductInfo': str(result.ProductInfo),
                'ProductAttributes': str(result.ProductAttributes),
                'ProductProvince': str(result.ProductProvince),
                'ProductCity': str(result.ProductCity),
                'ProductCountry': str(result.ProductCountry)
            }
            resp['result'] = tmp_data
        response = jsonify(resp)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    summnerNote = {}

    if PId != -1 and PId:
        summnerNote = Product.query.filter_by(PId=PId).first()

    summnerNote.ProductName = request.values['ProductName'] if 'ProductName' in request.values else ''
    summnerNote.ProductCategory = int(request.values['ProductCategory']) if 'ProductCategory' in request.values else ''
    summnerNote.ProductInfo = request.values['ProductInfo'] if 'ProductInfo' in request.values else ''
    summnerNote.Productsku = request.values['Productsku'] if 'Productsku' in request.values else ''
    summnerNote.ProductFormat = request.values['ProductFormat'] if 'ProductFormat' in request.values else ''
    summnerNote.ProductImage = request.values['ProductImage'] if 'ProductImage' in request.values else ''
    summnerNote.ProductAttributes = request.values['ProductAttributes'] if 'ProductAttributes' in request.values else ''
    summnerNote.ProductProvince = request.values['ProductProvince'] if 'ProductProvince' in request.values else ''
    summnerNote.ProductCity = request.values['ProductCity'] if 'ProductCity' in request.values else ''
    summnerNote.ProductCountry = request.values['ProductCountry'] if 'ProductCountry' in request.values else ''

    db.session.add(summnerNote)
    db.session.commit()

    response = jsonify(resp)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


# 添加商品
@route_account.route('/addproduct/', methods=['GET', 'POST'])
def addproduct():
    resp = {'code': 200, 'msg': '添加成功~'}

    summnerNote = Product()

    summnerNote.ProductName = request.values['ProductName'] if 'ProductName' in request.values else ''
    summnerNote.ShopId = request.values['ShopId'] if 'ShopId' in request.values else 1
    summnerNote.AId = request.values['AId'] if 'AId' in request.values else 1
    summnerNote.ProductMerchanName = request.values[
        'ProductMerchanName'] if 'ProductMerchanName' in request.values else '胡桃夹子'
    summnerNote.ProductCategory = int(request.values['ProductCategory']) if 'ProductCategory' in request.values else ''
    summnerNote.ProductInfo = request.values['ProductInfo'] if 'ProductInfo' in request.values else ''
    summnerNote.Productsku = request.values['Productsku'] if 'Productsku' in request.values else ''
    summnerNote.ProductFormat = request.values['ProductFormat'] if 'ProductFormat' in request.values else ''
    summnerNote.ProductImage = request.values['ProductImage'] if 'ProductImage' in request.values else ''
    summnerNote.ProductAttributes = request.values['ProductAttributes'] if 'ProductAttributes' in request.values else ''
    summnerNote.ProductProvince = request.values['ProductProvince'] if 'ProductProvince' in request.values else ''
    summnerNote.ProductCity = request.values['ProductCity'] if 'ProductCity' in request.values else ''
    summnerNote.ProductCountry = request.values['ProductCountry'] if 'ProductCountry' in request.values else ''
    summnerNote.ProductSold = 0
    db.session.add(summnerNote)
    db.session.commit()

    response = jsonify(resp)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

# 删除商品
@route_account.route('/deleteproduct/', methods=['GET', 'POST'])
def deleteproduct():
    resp = {'code': 200, 'msg': '删除成功'}

    PId = request.values['PId'] if 'PId' in request.values else -1

    result = Product.query.filter_by(PId=PId).first()
    db.session.delete(result)
    db.session.commit()

    response = jsonify(resp)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

# 图片接口
@route_account.route('/upload_img/', methods=['GET', 'POST'])
def upload_img():
    resp = {'status': 1, 'message': '文件上传成功'}
    image = request.files['file']
    file_path = os.path.join('Images/', image.filename)
    save_path = os.path.join(app.config["ABS_UPLOAD_FOLDER"], image.filename)
    image.save(save_path)
    result = UrlManager.buildImageUrl(file_path)
    resp['img'] = result
    response = jsonify(resp)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
