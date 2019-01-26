from flask import request, jsonify
from common.models.product import Product
from sqlalchemy import or_
from web.wechat_controllers import route_wechat

@route_wechat.route("/home/", methods=['GET', 'POST'])
def home():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values

    info = str(req['mix_kw']) if 'mix_kw' in req else ''
    page = int(req['page']) if 'page' in req else 1

    if page < 1:
        page = 1

    page_size = 10
    offset = (page - 1) * page_size
    query = Product.query.filter_by()

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
                'ProdectPrice': str(item.ProdectPrice),
                'ProductImage': str(item.ProductImage),
                'ProductStock': int(item.ProductStock),
                'ProductSold': str(item.ProductSold)
            }
            data_food_list.append(tmp_data)
    resp['data']['list'] = data_food_list
    resp['data']['has_more'] = 0 if len(data_food_list) < page_size else 1
    return jsonify(resp)

@route_wechat.route("/productInfo/", methods=['GET', 'POST'])
def productInfo():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values

    id = int(req['id']) if 'id' in req else 1

    productinfo = Product.query.filter_by(Id=id).first()

    data_food_list = []
    if productinfo:
        tmp_data = {
            'id': productinfo.Id,
            'ProductName': "%s" % (productinfo.ProductName),
            'ProductMerchantId': "%s" % (productinfo.ProductMerchantId),
            'ProductMerchanName': "%s" % (productinfo.ProductMerchanName),
            'ProductInfo': "%s" % (productinfo.ProductInfo),
            'ProdectPrice': str(productinfo.ProdectPrice),
            'ProductImage': str(productinfo.ProductImage),
            'ProductStock': int(productinfo.ProductStock),
            'ProductSold': str(productinfo.ProductSold)
        }
        data_food_list.append(tmp_data)
    resp['data'] = data_food_list
    return jsonify(resp)
