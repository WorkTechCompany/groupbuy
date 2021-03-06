from web.wechat_controllers import route_wechat
from application import app, db
from flask import request, jsonify
from sqlalchemy import or_
from common.models.order import Order
from common.models.pay.PayOrder import PayOrder
from common.models.pay.PayOrderItem import PayOrderItem
from common.models.product import Product
from common.models.shopping_trolley import ShoppingTrolley
from common.models.address import Address
from common.libs.pay.wechatService import WeChatService
from common.models.customer_login import CustomerLogin
from common.models.Balacelog.Balancelog import Balancelog
# from common.libs.cart.cartService import CartService
from common.models.shop_sale_change_log import ShopSaleChangeLog
from common.models.shop import Shop
from common.models.apply import Apply
from common.models.customer import Customer
from common.libs.Helper import getCurrentDate, getFormatDate
from common.libs.pay.PayService import PayService
import json
import logging
from logging.handlers import RotatingFileHandler
#
#
#
log_file = 'wechat.log'
root_logging = logging.getLogger()
root_logging.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s [%(name)s:%(filename)s:%(lineno)d] [%(levelname)s]- %(message)s')
# 文件最大2M
rotating_file_log = RotatingFileHandler(log_file, maxBytes=10485760, backupCount=3)
rotating_file_log.setLevel(logging.INFO)
rotating_file_log.setFormatter(formatter)
root_logging.addHandler(rotating_file_log)

@route_wechat.route("/showorder/", methods=['POST'])
def showorder():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values

    Cid = int(req['Cid']) if 'Cid' in req else -1
    page = int(req['page']) if 'page' in req else 1
    OrderStatus = int(req['OrderStatus']) if 'OrderStatus' in req else -1

    if Cid == -1:
        resp['code'] = -1
        resp['msg'] = '账户错误'
        response = jsonify(resp)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    if page < 1:
        page = 1

    page_size = 10
    offset = (page - 1) * page_size
    if Cid:
        query = PayOrder.query.filter_by(member_id=Cid)
    # 待付款：1   申请退款 待付款
    if OrderStatus == 1:
        query = query.filter_by(status=-8)
    if OrderStatus == 2:
        query = query.filter(or_(PayOrder.status == -7, PayOrder.status == -6, PayOrder.status==1))
    if OrderStatus == 3:
        query = query.filter(or_(PayOrder.status == 0, PayOrder.status == -5))

    totalCount = query.count()

    order_list = query.order_by(PayOrder.id.desc()) \
        .offset(offset).limit(page_size).all()

    o_list = []
    if order_list:
        for item in order_list:
            pay_order_item_query = PayOrderItem.query.filter_by(pay_order_id=int(item.id))
            pay_order_item = pay_order_item_query.order_by(PayOrderItem.id.desc()).all()
            data_list = []
            for info in pay_order_item:
                Product_info = Product.query.filter_by(Pid=info.Pid).first()
                # data_list['OrderStatus'] = item.status
                tmp_data = {
                    'id': item.id,   # 订单id
                    'Pid': info.Pid,
                    'Cid': item.member_id,
                    'order_sn': item.order_sn,
                    'Shopid': Product_info.Shopid,
                    'ProductName': str(Product_info.ProductName),
                    'OrderCount': str(info.quantity),
                    # 'OrderFormat': str(item.OrderFormat),
                    'ProductImage': str(Product_info.ProductImage),
                    'OrderPrice': str(info.price),
                    'total_price': str(item.total_price),
                    'OrderTime': str(item.updated_time),
                    'OrderStatus': str(item.status),
                    'tracking_number': str(item.tracking_number)
                }
                data_list.append(tmp_data)
            o_list.append(data_list)
    resp['totalCount'] = totalCount
    resp['data']['list'] = o_list
    resp['data']['has_more'] = 0 if len(o_list) < page_size else 1
    response = jsonify(resp)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@route_wechat.route("/orderinfo/", methods=['POST'])
def orderinfo():
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}, 'OrderAddressInfo': {}, 'pay_price': {}}
    req = request.values

    id = int(req['id']) if 'id' in req else -1

    Pay_info = PayOrder.query.filter_by(id=id).first()
    OrderInfo = PayOrderItem.query.filter_by(pay_order_id=id).all()


    if OrderInfo:
        AddressInfo = Pay_info.express_address_id
        AddressInfo = Address.query.filter_by(Id=AddressInfo).first()
        address = {
            'id': AddressInfo.Id,
            'Cid': AddressInfo.Cid,
            'Addressee': AddressInfo.Addressee,
            'AddresseePhone': AddressInfo.AddresseePhone,
            'Province': AddressInfo.Province,
            'City': AddressInfo.City,
            'County': AddressInfo.County,
            'Details': AddressInfo.Details,
            'Status': int(AddressInfo.Status)
        }
        data_list = []
        for item in OrderInfo:
            ProductInfo = Product.query.filter_by(Pid=item.Pid).first()
            tmp_data = {
                'Oid': item.pay_order_id,
                'Pid': item.Pid,
                'Shopid': ProductInfo.Shopid,
                'ProductName': "%s" % (ProductInfo.ProductName),
                'OrderCount': "%s" % (item.quantity),
                'ProductImage': "%s" % (ProductInfo.ProductImage),
                'OrderPrice': "%s" % (item.price),
                'OrderTime': getFormatDate(item.updated_time),
                'OrderStatus': int(Pay_info.status),
                'tracking_number': str(Pay_info.tracking_number)
                # 'OrderAddressInfo': address
            }
            data_list.append(tmp_data)
        resp['data'] = data_list
        resp['OrderAddressInfo'] = address
        resp['pay_price'] = str(Pay_info.pay_price)
    return jsonify(resp)

# @route_wechat.route("/showorder/", methods=["POST"])
# def showorder():
#
#     resp = {'code': 200, 'msg': "操作成功", 'data': {}}
#     req = request.values
#     params_goods = req['goods'] if 'goods' in req else None
#
#     member_info = g.member_info
#     goods_list = []
#     if params_goods:
#         goods_list = json.loads(params_goods)
#
#     food_dic = {}
#     for item in goods_list:
#         food_dic[item['id']] = item['number']
#
#     food_ids = food_dic.keys()
#     food_list = Food.query.filter(Food.id.in_(food_ids)).all()
#     data_food_list = []
#
#     yun_price = pay_price = decimal.Decimal(0.00)
#     if food_list:
#         for item in food_list:
#             tmp_data = {
#                 'id': item.id,
#                 'name': item.name,
#                 'price': str(item.price),
#                 'pic_url': UrlManager.buildImageUrl(item.main_image),
#                 'number':  food_dic[item.id]
#             }
#             pay_price = pay_price + item.price * int(food_dic[item.id])
#             data_food_list.append(tmp_data)
#
#     # 获取地址
#     address_info = MemberAddress.query.filter_by(is_default=1, member_id=member_info.id, status=1).first()
#     default_address = ''
#     if address_info:
#         default_address = {
#             "id": address_info.id,
#             "name": address_info.nickname,
#             "mobile": address_info.mobile,
#             "address": "%s%s%s%s" % (
#             address_info.province_str, address_info.city_str, address_info.area_str, address_info.address)
#         }
#     resp['data']['food_list'] = data_food_list
#     resp['data']['pay_price'] = str(pay_price)
#     resp['data']['yun_price'] = str(yun_price)
#     resp['data']['total_price'] = str(pay_price + yun_price)
#     resp['data']['default_address'] = default_address
#     return jsonify(resp)

@route_wechat.route("/placeorder/", methods=["POST"])
def orderCreate():

    resp = {'code': 200, 'msg': "下单成功", 'data': {}}
    req = request.values

    Cid = int(req['Cid']) if 'Cid' in req and req['Cid'] else 0
    Shopid = int(req['Shopid']) if 'Shopid' in req and req['Shopid'] else 0
    trolley_result = req['trolley_list'] if 'trolley_list' in req else ''
    OrderAddress = req['OrderAddress'] if 'OrderAddress' in req else ''
    params_goods = req['params_goods'] if 'params_goods' in req else None

    items = []
    if params_goods:
        items = json.loads(params_goods)

    if len(items) < 1:
        resp['code'] = -1
        resp['msg'] = "下单失败: 没有选择商品"
        return jsonify(resp)

    address_info = Address.query.filter_by(Id=OrderAddress).first()
    if not address_info:
        resp['code'] = -1
        resp['msg'] = "下单失败：快递地址不对~~"
        return jsonify(resp)

    target = PayService()

    params = {
        # 地址id
        'express_address_id': address_info.Id,
        # 地址信息
        'express_info': {
            'mobile': address_info.AddresseePhone,
            'nickname': address_info.Addressee,
            "address": "%s%s%s%s" % (
            address_info.Province, address_info.City, address_info.County, address_info.Details)
        }
    }
    resp = target.createOrder(Cid, Shopid, items, params=params)

    if resp['code'] == 200:
        if trolley_result != '':
            trolley_list = trolley_result.strip(',').split(',')
            if trolley_list:
                for item in trolley_list:
                    result = ShoppingTrolley.query.filter_by(Id=int(item)).first()
                    db.session.delete(result)
                    db.session.commit()
    return jsonify(resp)

@route_wechat.route("/balancepay/", methods=["POST"])
def balancepay():

    # 余额支付
    # 通过订单查询价格
    # 扣除余额

    resp = {'code': 200, 'msg': "操作成功", 'data': {}}
    req = request.values
    id = req['id'] if 'id' in req else ''
    order_sn = req['order_sn'] if 'order_sn' in req else ''
    Cid = req['Cid'] if 'Cid' in req else ''

    pay_order_info = PayOrder.query.filter_by(order_sn=order_sn).first()
    if not pay_order_info:
        resp['code'] = -1
        resp['code'] = "系统繁忙"
        return jsonify(resp)

    oauth_bind_info = CustomerLogin.query.filter_by(Cid=Cid).first()
    if not oauth_bind_info:
        resp['code'] = -1
        resp['code'] = "系统繁忙"
        return jsonify(resp)

    pay_order_info = PayOrder.query.filter_by(order_sn=order_sn).first()
    if not pay_order_info or pay_order_info.status not in [-8, -7]:
        resp['code'] = -1
        resp['code'] = "已支付"
        return jsonify(resp)

    Customer_info = Customer.query.filter_by(Cid=Cid).first()
    pay_price = float(pay_order_info.total_price)
    MyBalance = float(Customer_info.MyBalance)
    if pay_price > MyBalance:
        resp['code'] = -1
        resp['code'] = "余额不足"
        return jsonify(resp)

    # 更改订单状态
    pay_order_info.status = 1
    pay_order_info.express_status = -7
    pay_order_info.updated_time = getCurrentDate()
    pay_order_info.pay_time = getCurrentDate()
    db.session.add(pay_order_info)

    # 扣除余额
    info = Customer.query.filter_by(Cid=Cid).first()
    mybalance = float(info.MyBalance)
    result = float(pay_order_info.total_price)
    mybalance = mybalance - result
    info.MyBalance = mybalance
    db.session.add(info)

    # 售卖记录
    pay_order_items = PayOrderItem.query.filter_by(id=id).all()
    for order_item in pay_order_items:
        tmp_model_sale_log = ShopSaleChangeLog()
        tmp_model_sale_log.Pid = order_item.Pid
        tmp_model_sale_log.quantity = order_item.quantity
        tmp_model_sale_log.price = order_item.price
        tmp_model_sale_log.member_id = order_item.member_id
        tmp_model_sale_log.created_time = getCurrentDate()

        db.session.add(tmp_model_sale_log)

    # 流水记录
    Balance_log = Balancelog()

    Balance_log.BankCardNumber = -1000
    Balance_log.Cid = pay_order_info.member_id
    Balance_log.Openingbank = -1000
    Balance_log.balance = pay_order_info.total_price
    Balance_log.operating = 2
    Balance_log.status = 4
    Balance_log.total_balance = pay_order_info.total_price
    Balance_log.receipt_qrcode = pay_order_info.order_sn
    Balance_log.freeze_balance = pay_order_info.total_price
    Balance_log.Accountname = -1000
    Balance_log.createtime = getCurrentDate()
    Balance_log.updatetime = getCurrentDate()
    db.session.add(Balance_log)

    db.session.commit()
    return jsonify(resp)


@route_wechat.route("/pay/", methods=["POST"])
def pay():

    resp = {'code': 200, 'msg': "操作成功", 'data': {}}
    req = request.values

    order_sn = req['order_sn'] if 'order_sn' in req else ''
    Cid = req['Cid'] if 'Cid' in req else ''
    pay_order_info = PayOrder.query.filter_by(order_sn=order_sn).first()
    if not pay_order_info:
        resp['code'] = -1
        resp['code'] = "系统繁忙"
        return jsonify(resp)

    oauth_bind_info = CustomerLogin.query.filter_by(Cid=Cid).first()
    if not oauth_bind_info:
        resp['code'] = -1
        resp['code'] = "系统繁忙"
        return jsonify(resp)

    config_mina = app.config["MINA_APP"]
    notify_url = app.config["APP"]["domain"] + config_mina['callback_url']
    target_wechat =WeChatService(merchant_key=config_mina["paykey"])

    data = {
        'appid': config_mina['appid'],
        'mch_id': config_mina['mch_id'],
        'nonce_str': target_wechat.get_nonce_str(),
        'body': "购买",
        'out_trade_no': pay_order_info.order_sn,
        'total_fee': int(pay_order_info.total_price * 100),
        'spbill_create_ip': '132.232.139.186',
        'notify_url': notify_url,
        'trade_type': 'JSAPI',
        'openid': oauth_bind_info.openid
    }

    logging.info(data)

    pay_info = target_wechat.get_pay_info(data)


    # 保存prepay_id
    pay_order_info.prepay_id = pay_info['prepay_id']
    db.session.add(pay_order_info)
    db.session.commit()

    resp['data']['pay_info'] = pay_info

    return jsonify(resp)

@route_wechat.route("/callback/", methods=["POST"])
def callback():
    logging.info('进入回调函数')
    result_data = {
        'return_code': 'SUCCESS',
        'return_msg': 'OK'
    }

    header = {'Content-Type':'application/xml'}
    config_mina = app.config['MINA_APP']

    logging.info(request.data)

    target_wechat = WeChatService(merchant_key=config_mina['paykey'])
    # print(request.data)

    callback_data = target_wechat.xml_to_dict(request.data)

    sign = callback_data['sign']
    callback_data.pop('sign')
    gene_sign = target_wechat.create_sign(callback_data)

    if sign != gene_sign:
        # logging.info('sing!=gene_sign')
        result_data['return_code'] = result_data['return_msg'] = "FAIL"
        return target_wechat.dict_to_xml(result_data), header

    order_sn = callback_data['out_trade_no']
    pay_order_info = PayOrder.query.filter_by(order_sn=order_sn).first()
    if not pay_order_info:
        # logging.info('not pay_order_info')
        result_data['return_code'] = result_data['return_msg'] = "FAIL"
        return target_wechat.dict_to_xml(result_data), header

    # if int(pay_order_info.total_price * 100) == int(callback_data['total_fee']):
    #     result_data['return_code'] = result_data['return_msg'] = "FAIL"
    #     return target_wechat.dict_to_xml(result_data), header

    if pay_order_info.status == 1:
        # logging.info('pay_order_info.status == 1')
        return target_wechat.dict_to_xml(result_data), header

    target_pay = PayService()
    target_pay.orderSuccess(pay_order_info.id, params={'pay_sn': callback_data['transaction_id']})

    # 微信回调加入日志
    target_pay.addPayCallbackData(pay_order_id=pay_order_info.id, data=request.data)

    return target_wechat.dict_to_xml(result_data), header

# @route_wechat.route("/placeorder/", methods=['POST'])
# def placeorder():
#     resp = {'code': 200, 'msg': '下单成功'}
#     trolley_result = request.values['trolley_list']
#     if trolley_result:
#         trolley_list = trolley_result.strip(',').split(',')
#         if trolley_list:
#             for item in trolley_list:
#                 result = ShoppingTrolley.query.filter_by(Id=int(item)).first()
#                 db.session.delete(result)
#                 db.session.commit()
#
#     result = json.loads(request.values['order_list'])
#     for item in result:
#         summnerNote = Order()
#         summnerNote.Pid = item['Pid'] if 'Pid' in item else ''
#         summnerNote.Cid = item['Cid'] if 'Cid' in item else ''
#         summnerNote.Shopid = item['Shopid'] if 'Shopid' in item else -1
#         summnerNote.ProductName = item['ProductName'] if 'ProductName' in item else ''
#         summnerNote.OrderCount = item['OrderCount'] if 'OrderCount' in item else ''
#         # summnerNote.OrderFormat = request.values['OrderFormat'] if 'OrderFormat' in request.values else ''
#         summnerNote.ProductImage = item['ProductImage'] if 'ProductImage' in item else ''
#         price = item['OrderPrice'] if 'OrderPrice' in item else 0
#         summnerNote.OrderPrice = float('%.2f' % (float(price) * int(summnerNote.OrderCount)))
#         summnerNote.OrderAddress = item['OrderAddress'] if 'OrderAddress' in item else ''
#         summnerNote.OrderRefund = ''
#         summnerNote.OrderExpress = -1
#         summnerNote.OrderTime = getCurrentDate()
#         summnerNote.OrderStatus = 1
#         summnerNote.OrderRefundStatus = 0
#
#         db.session.add(summnerNote)
#         db.session.commit()
#
#     return jsonify(resp)


@route_wechat.route("/orderRefund/", methods=['POST'])
def orderRefund():
    resp = {'code': 200, 'msg': '申请成功，1~3个工作日内进行审核！'}
    req = request.values

    Oid = int(req['Oid']) if 'Oid' in req else -1
    OrderRefund = req['OrderRefund'] if 'OrderRefund' in req else -1
    OrderRefundStatus = 2

    result = Order.query.filter_by(Oid=Oid).first()
    result.OrderRefundStatus = int(OrderRefundStatus)
    result.OrderExpress = str(OrderRefund)

    db.session.commit()
    response = jsonify(resp)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@route_wechat.route("/deleteorder/", methods=['GET', 'POST'])
def deleteorder():
    resp = {'code': 200, 'msg': '取消成功'}

    id = request.values['id'] if 'id' in request.values else -1
    result = PayOrder.query.filter_by(id=id).first()
    result.status = 0

    # 返回库存
    pay_order_item_info = PayOrderItem.query.filter_by(pay_order_id=result.id).all()
    for item in pay_order_item_info:
        product_info = Product.query.filter_by(Pid=item.Pid).first()
        stock = int(product_info.ProductStock)
        stock_result = stock + int(item.quantity)
        product_info.ProductStock = stock_result

    db.session.commit()
    return jsonify(resp)

@route_wechat.route("/confirmorder/", methods=['GET', 'POST'])
def confirmorder():
    resp = {'code': 200, 'msg': '确认成功'}

    id = request.values['id'] if 'id' in request.values else -1
    result = PayOrder.query.filter_by(id=id).first()
    result.status = 0

    db.session.commit()
    return jsonify(resp)


@route_wechat.route("/confirmreceipt/", methods=['POST'])
def confirmreceipt():


    # 确认收货
    # 用户冻结金额清零
    # 商户余额增加加入记录

    resp = {'code': 200, 'msg': '确认收货成功'}

    Oid = request.values['Oid'] if 'Oid' in request.values else -1
    Shopid = request.values['Shopid'] if 'Shopid' in request.values else -1

    Pay_info = PayOrder.query.filter_by(id=Oid).first()
    Pay_info.status = -5
    loginfo = Balancelog.query.filter_by(receipt_qrcode=Pay_info.order_sn).first()
    Shop_info = Shop.query.filter_by(Shopid=Shopid).first()
    Apply_info = Apply.query.filter_by(Aid=Shop_info.Aid).first()
    # 商户Cid
    Customer_info = Customer.query.filter_by(Cid=Apply_info.Cid).first()

    # 用户冻结金额清零
    freeze_balance = loginfo.freeze_balance
    loginfo.freeze_balance = float(0)

    mybalance = float(Customer_info.MyBalance)
    result = float(freeze_balance)
    mybalance = mybalance + result
    Customer_info.MyBalance = mybalance

    # 销量增加
    pay_order_item_info = PayOrderItem.query.filter_by(pay_order_id=Pay_info.id).all()
    for item in pay_order_item_info:
        product_info = Product.query.filter_by(Pid=item.Pid).first()
        sold = int(product_info.ProductSold)
        sold_result = sold + item.quantity
        product_info.ProductSold = sold_result

    # 打款给商家记录
    Balance_log = Balancelog()

    Balance_log.BankCardNumber = -1000
    Balance_log.Cid = Customer_info.Cid
    Balance_log.Openingbank = -1000
    Balance_log.balance = freeze_balance
    Balance_log.operating = 4
    Balance_log.status = 6
    Balance_log.total_balance = freeze_balance
    target_pay = PayService()
    Balance_log.receipt_qrcode = target_pay.geneOrderSn()
    Balancelog.freeze_balance = float(0)
    Balance_log.Accountname = -1000
    Balance_log.createtime = getCurrentDate()
    Balance_log.updatetime = getCurrentDate()
    db.session.add(Balance_log)

    db.session.commit()
    response = jsonify(resp)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
