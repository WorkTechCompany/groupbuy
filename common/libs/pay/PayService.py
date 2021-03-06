import decimal, hashlib, time, random ,json
from application import db, app

# from common.models.food.Food import Food
from common.models.pay.PayOrder import PayOrder
from common.models.pay.PayOrderCallbackData import PayOrderCallbackData
from common.models.pay.PayOrderItem import PayOrderItem
from common.libs.Helper import getCurrentDate
from common.models.product import Product
from common.models.customer import Customer
from common.libs.product.ProductService import ProductService
from common.libs.queue.queueService import QueueService
from common.models.shop_sale_change_log import ShopSaleChangeLog
from common.models.Balacelog.Balancelog import Balancelog

class PayService():
    def __init__(self):
        pass

    def createOrder(self, Cid, Shopid, items=None, params=None, recharge=None):
        resp = {'code': 200, 'msg': "操作成功", 'data': {}}

        pay_price = decimal.Decimal(0.00)
        continue_count = 0
        product_id = []
        for item in items:
            if decimal.Decimal(item['price']) < 0:
                continue_count += 1
                continue
            pay_price = pay_price + decimal.Decimal(item['price']) * int(item['number'])
            if recharge != 'recharge':
                product_id.append(item['Pid'])

        if continue_count >= len(items):
            resp['code'] = -1
            resp['msg'] = "商品为空"
            return resp

        yun_price = params['yun_price'] if 'yun_price' in params else 0
        # note = params['note'] if 'note' in params else 0
        express_address_id = params['express_address_id'] if params and 'express_address_id' in params else 0
        express_info = params['express_info'] if params and 'express_info' in params else {}

        yun_price = decimal.Decimal(yun_price)
        total_price = yun_price + pay_price

        # 并发处理
        try:
            # 开启事务
            tmp_product_list = db.session.query(Product).filter(Product.Pid.in_(product_id)).with_for_update().all()

            tmp_product_stock_mapping = {}
            for tmp_item in tmp_product_list:
                tmp_product_stock_mapping[tmp_item.Pid] = tmp_item.ProductStock

            #支付订单
            model_pay_order = PayOrder()
            model_pay_order.member_id = Cid
            model_pay_order.Shopid = Shopid
            model_pay_order.order_sn = self.geneOrderSn()
            model_pay_order.total_price = total_price
            model_pay_order.yun_price = yun_price
            model_pay_order.pay_price = pay_price
            # model_pay_order.note = note
            if recharge != 'recharge':
                model_pay_order.status = -8
                model_pay_order.express_status = -8
            else:
                model_pay_order.status = 11
                model_pay_order.express_status = 11
            model_pay_order.express_address_id = express_address_id
            model_pay_order.express_info = json.dumps(express_info)
            model_pay_order.updated_time = model_pay_order.created_time = getCurrentDate()
            db.session.add(model_pay_order)



            for item in items:
                if recharge != 'recharge':

                    tmp_left_stock = tmp_product_stock_mapping[item['Pid']]
                    if decimal.Decimal(item['price']) < 0:
                        continue
                    if int(item['number']) > int(tmp_left_stock):
                        raise Exception("该商品剩余: %s" % (tmp_left_stock))

                    result = int(tmp_left_stock) - int(item['number'])
                    tmp_ret = Product.query.filter_by(Pid=item['Pid']).update({
                        'ProductStock': int(result)
                    })

                    if not tmp_ret:
                        raise Exception("下单失败")
                    tmp_pay_item = PayOrderItem()
                    tmp_pay_item.pay_order_id = model_pay_order.id
                    tmp_pay_item.member_id = Cid
                    tmp_pay_item.quantity = item['number']
                    tmp_pay_item.price = item['price']
                    tmp_pay_item.Pid = item['Pid']
                    # tmp_pay_item.note = note
                    tmp_pay_item.updated_time = tmp_pay_item.created_time = getCurrentDate()
                    if recharge != 'recharge':
                        ProductService.setStockChangeLog(item['Pid'], result)
                    db.session.add(tmp_pay_item)

            # 提交事务
            db.session.commit()
            resp['data'] = {
                'id': model_pay_order.id,
                'order_sn': model_pay_order.order_sn,
                'total_price': str(model_pay_order.total_price)
            }

        except Exception as e:
            db.session.rollback()
            print(e)
            resp['code'] = -1
            resp['msg'] = "下单失败请重新下单"
            resp['msg'] = str(e)

        return resp

    def orderSuccess(self, pay_order_id = 0,params =None):
        try:
            pay_order_info = PayOrder.query.filter_by(id =pay_order_id).first()
            if not pay_order_info or pay_order_info.status not in [-8, -7]:
                return True

            pay_order_info.pay_sn = params['pay_sn']
            pay_order_info.status = 1
            pay_order_info.express_status = -7
            pay_order_info.updated_time = getCurrentDate()
            pay_order_info.pay_time = getCurrentDate()
            db.session.add(pay_order_info)


            # 售卖记录
            pay_order_items = PayOrderItem.query.filter_by(pay_order_id=pay_order_id).all()
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
        except Exception as e:
            print(e)
            db.session.rollback()
            return False

        QueueService.addQueue("pay", {
            "Cid": pay_order_info.member_id,
            "pay_order_id": pay_order_info.id
        })

    def rechargeorderSuccess(self, member_id=-1, pay_order_id = 0,params =None):
        try:
            pay_order_info = PayOrder.query.filter_by(id =pay_order_id).first()
            if not pay_order_info or pay_order_info.status not in [11]:
                return True

            pay_order_info.pay_sn = params['pay_sn']
            pay_order_info.status = 12
            pay_order_info.express_status = 12
            pay_order_info.updated_time = getCurrentDate()
            pay_order_info.pay_time = getCurrentDate()
            db.session.add(pay_order_info)

            Customer_info = Customer.query.filter_by(Cid =member_id).first()
            money = Customer_info.MyBalance
            money += pay_order_info.total_price
            Customer_info.MyBalance = money
            db.session.add(Customer_info)

            # 充值记录
            pay_order_items = PayOrderItem.query.filter_by(pay_order_id=pay_order_id).all()
            for order_item in pay_order_items:
                tmp_model_sale_log = ShopSaleChangeLog()
                tmp_model_sale_log.Pid = 100000
                tmp_model_sale_log.quantity = 1
                tmp_model_sale_log.price = order_item.price
                tmp_model_sale_log.member_id = order_item.member_id
                tmp_model_sale_log.created_time = getCurrentDate()

                db.session.add(tmp_model_sale_log)

            # 充值流水记录
            # 流水记录
            Balance_log = Balancelog()

            Balance_log.BankCardNumber = -1000
            Balance_log.Cid = pay_order_info.member_id
            Balance_log.Openingbank = -1000
            Balance_log.balance = pay_order_info.total_price
            Balance_log.operating = 3
            Balance_log.status = 5
            Balance_log.total_balance = pay_order_info.total_price
            Balance_log.receipt_qrcode = pay_order_info.order_sn
            Balancelog.freeze_balance = pay_order_info.total_price
            Balance_log.Accountname = -1000
            Balance_log.createtime = getCurrentDate()
            Balance_log.updatetime = getCurrentDate()
            db.session.add(Balance_log)

            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return False

        QueueService.addQueue("pay", {
            "Cid": pay_order_info.member_id,
            "pay_order_id": pay_order_info.id
        })

    def addPayCallbackData(self, pay_order_id=0, type ='pay', data=''):
        model_paycallback = PayOrderCallbackData()
        model_paycallback.pay_order_id = pay_order_id
        if type == "pay":
            model_paycallback.pay_data = data
            model_paycallback.refund_data = ''
        else:
            model_paycallback.pay_data = ''
            model_paycallback.refund_data = data
        model_paycallback.created_time = model_paycallback.updated_time = getCurrentDate()

        db.session.add(model_paycallback)
        db.session.commit()
        return True


    def geneOrderSn(self):
        m = hashlib.md5()
        sn = None
        while True:
            str = "%s-%s" % (int(round(time.time() * 1000)), random.randint(0, 9999999))
            m.update(str.encode("utf-8"))
            sn = m.hexdigest()
            # print(PayOrder.query.filter_by(order_sn = sn).first())
            if not PayOrder.query.filter_by(order_sn = sn).first():
                break

        return sn
    #
    #
    # def closeOrder(self,pay_order_id = 0):
    #     if pay_order_id < 1:
    #         return False
    #     pay_order_info = PayOrder.query.filter_by( id =  pay_order_id ,status = -8 ).first()
    #     if not pay_order_info:
    #         return False
    #
    #     pay_order_items = PayOrderItem.query.filter_by( pay_order_id = pay_order_id ).all()
    #     if pay_order_items:
    #         #需要归还库存
    #         for item in pay_order_items:
    #             tmp_food_info = Food.query.filter_by( id = item.food_id ).first()
    #             if tmp_food_info:
    #                 tmp_food_info.stock = tmp_food_info.stock + item.quantity
    #                 tmp_food_info.updated_time = getCurrentDate()
    #                 db.session.add( tmp_food_info )
    #                 db.session.commit()
    #                 FoodService.setStockChangeLog( item.food_id, item.quantity, "订单取消")
    #
    #     pay_order_info.status = 0
    #     pay_order_info.updated_time = getCurrentDate()
    #     db.session.add( pay_order_info )
    #     db.session.commit()
    #     return True