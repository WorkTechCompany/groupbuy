from flask import request, jsonify
from common.models.product import Product
from sqlalchemy import or_
from web.wechat_controllers import route_wechat
import json

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

    shop_list = query.order_by(Product.PId.desc()) \
        .offset(offset).limit(page_size).all()

    data_food_list = []
    if shop_list:
        for item in shop_list:
            price = json.loads(item.ProductFormat)[0]['price']
            stock = json.loads(item.ProductFormat)[0]['stock']
            tmp_data = {
                'PId': item.PId,
                'ProductName': "%s" % (item.ProductName),
                'ShopId': "%s" % (item.ShopId),
                'ProdectPrice': str(price),
                'ProductImage': str(item.ProductImage),
                'ProductStock': int(stock),
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

    PId = int(req['PId']) if 'PId' in req else -1

    productinfo = Product.query.filter_by(PId=PId).first()

    if productinfo:
        tmp_data = {
            'PId': productinfo.PId,
            'ProductName': "%s" % (productinfo.ProductName),
            'ShopId': "%s" % (productinfo.ShopId),
            'ProductMerchanName': "%s" % (productinfo.ProductMerchanName),
            'ProductInfo': "%s" % (productinfo.ProductInfo),
            'ProductFormat': str(productinfo.ProductFormat),
            'ProductImage': str(productinfo.ProductImage),
            'ProductSold': str(productinfo.ProductSold)
        }
        resp['data'] = tmp_data
    return jsonify(resp)
    # PId = db.Column(db.BigInteger, primary_key=True)                                                        # 商品ID
    # ProductName = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())              # 商品名称
    # ShopId = db.Column(db.BigInteger, nullable=False, server_default=db.FetchedValue())                     # 商店ID
    # AId = db.Column(db.BigInteger, nullable=False, server_default=db.FetchedValue())                        # 商户ID
    # ProductMerchanName = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())        # 商品店主名字
    # ProductCategory = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())           # 商品分类
    # ProductInfo = db.Column(db.String(5000), nullable=False, server_default=db.FetchedValue())             # 商品信息
    # ProductSold = db.Column(Integer, nullable=False, server_default=db.FetchedValue())                     # 商品已售数
    # ProductFormat = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())           # 商品规格
    # ProductImage = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())           # 商品图片
    # ProductAttributes = db.Column(db.BigInteger, nullable=False, server_default=db.FetchedValue())      # 销售属性
    # ProductProvince = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())            # 省份
    # ProductCity = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())                # 市区
    # ProductCountry = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())               # 县