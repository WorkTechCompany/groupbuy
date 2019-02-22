from flask import request, jsonify
from common.models.product import Product
from sqlalchemy import or_
from web.wechat_controllers import route_wechat
from common.models.shop import Shop
from common.models.pay.PayOrderItem import PayOrderItem
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
        rule = or_(Product.ProductName.ilike("%{0}%".format(info)))
        query = query.filter(rule)

    shop_list = query.order_by(Product.Pid.desc()) \
        .offset(offset).limit(page_size).all()

    data_food_list = []
    if shop_list:
        for item in shop_list:
            # price = json.loads(item.ProductFormat)[0]['price']
            # stock = json.loads(item.ProductFormat)[0]['stock']
            tmp_data = {
                'Pid': item.Pid,
                'Aid': item.Aid,
                'ProductName': "%s" % (item.ProductName),
                'Shopid': "%s" % (item.Shopid),
                'ProductPrice': str(item.ProductPrice),
                'ProductStock': int(item.ProductStock),
                'ProductImage': str(item.ProductImage),
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

    Pid = int(req['Pid']) if 'Pid' in req else -1

    productinfo = Product.query.filter_by(Pid=Pid).first()

    if productinfo:
        shop_info = []
        ShopInfo = Shop.query.filter_by(Shopid=productinfo.Shopid).first()
        shop = {
            'Shopid': ShopInfo.Shopid,
            'Aid': ShopInfo.Aid,
            'ShopName': ShopInfo.ShopName,
            'ShopImage': ShopInfo.ShopImage,
            'ShopCategory': ShopInfo.ShopCategory,
            'ShopProvince': ShopInfo.ShopProvince,
            'ShopCity': ShopInfo.ShopCity,
            'ShopCountry': ShopInfo.ShopCountry,
        }
        shop_info.append(shop)
        # customer_list = []
        # order_list = []
        # pay_order_items = PayOrderItem.query.filter_by(Pid=Pid).all()
        # for item in pay_order_items:
        #     order_list.append(item)
        tmp_data = {
            'Pid': productinfo.Pid,
            'Aid': productinfo.Aid,
            'ProductName': "%s" % (productinfo.ProductName),
            'ShopInfo': shop_info,
            'ProductMerchanName': "%s" % (productinfo.ProductMerchanName),
            'ProductInfo': "%s" % (productinfo.ProductInfo),
            'ProductPrice': str(productinfo.ProductPrice),
            'ProductStock': int(productinfo.ProductStock),
            'ProductImage': str(productinfo.ProductImage),
            'ProductSold': str(productinfo.ProductSold)
            # 'ProductBayCustomer': customer_list
        }
        resp['data'] = tmp_data
    return jsonify(resp)