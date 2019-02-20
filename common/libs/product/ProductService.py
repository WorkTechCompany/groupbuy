# -*- coding: utf-8 -*-
from application import app,db
from common.models.product import Product
from common.libs.Helper import getCurrentDate


class ProductService():

    @staticmethod
    def setStockChangeLog(Pid = 0, result = 0,note = '' ):

        if Pid < 1:
            return False

        product_info = Product.query.filter_by(Pid=Pid).first()
        if not product_info:
            return False

        product_info.ProductStock = result
        # model_stock_change = FoodStockChangeLog()
        # model_stock_change.food_id = food_id
        # model_stock_change.unit = quantity
        # model_stock_change.total_stock = food_info.stock
        # model_stock_change.note = note
        # model_stock_change.created_time = getCurrentDate()
        # db.session.add(model_stock_change)
        db.session.commit()
        return True


