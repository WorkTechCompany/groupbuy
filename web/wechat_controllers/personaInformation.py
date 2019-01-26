from web.wechat_controllers import route_wechat
from common.models.apply import Apply, db
from application import app, db
from flask import request, jsonify
from common.models.product import Product
import os
from common.models.address import Address
from common.libs.UrlManager import UrlManager


@route_wechat.route("/persion/", methods=['GET', 'POST'])
def persion():

    resp = {'code': 200, 'info': {}}
    req = request.values
    #
    if request.method == 'GET':
        Cid = req['Cid']
        info = Product.query.filter_by(Cid=Cid).first()
        resp['info'] = {
            'Cid': Cid,
            'CustomerName': info.CustomerName,
            'CustomerPhone': info.CustomerPhone,
            'MyBalance': info.MyBalance,
            'AvailableBalance': info.AvailableBalance,
            "MyIncome": info.MyIncome
        }
    return jsonify(resp)


@route_wechat.route("/apply/", methods=['POST'])
def apply():

    resp = {'code': 200, 'msg': '申请成功，将于三个工作日内进行审核~'}
    summnerNote = Apply()
    summnerNote.ShopCategory = request.values['ShopCategory'] if 'ShopCategory' in request.values else ''
    summnerNote.IdentityCard = request.values['IdentityCard'] if 'IdentityCard' in request.values else ''
    summnerNote.IdentityCardHand = request.values['IdentityCardHand'] if 'IdentityCardHand' in request.values else ''
    summnerNote.BusinessLicense = request.values['BusinessLicense'] if 'BusinessLicense' in request.values else ''
    summnerNote.Contract = request.values['Contract'] if 'Contract' in request.values else ''
    summnerNote.IDCard = request.values['IDCard'] if 'IDCard' in request.values else ''
    summnerNote.ApplyProvince = request.values['ApplyProvince'] if 'ApplyProvince' in request.values else ''
    summnerNote.ApplyCity = request.values['ApplyCity'] if 'ApplyCity' in request.values else ''
    summnerNote.ApplyCounty = request.values['ApplyCounty'] if 'ApplyCounty' in request.values else ''
    summnerNote.ApplyDetails = request.values['ApplyDetails'] if 'ApplyDetails' in request.values else ''
    summnerNote.ApplyPhone = request.values['ApplyPhone'] if 'ApplyPhone' in request.values else ''
    summnerNote.ApplyPassword = request.values['ApplyPassword'] if 'ApplyPassword' in request.values else ''
    summnerNote.ShopStatus = 0

    db.session.add(summnerNote)
    db.session.commit()

    return jsonify(resp)


@route_wechat.route("/showAddress/", methods=['POST'])
def showress():
    resp = {'code': 200, 'msg': '查询成功'}
    req = request.values
    Cid = req['Cid']
    result = Address.query.filter_by(Cid=Cid)
    # if not result:
    #     resp['code'] = -1
    #     resp['msg'] = '暂无地址'
    #     return jsonify(result)
    address_list = []
    for item in result:
        address = {
            'id': item.Id,
            'Cid': item.Cid,
            'Addressee': item.Addressee,
            'AddresseePhone': item.AddresseePhone,
            'Province': item.Province,
            'City': item.City,
            'County': item.County,
            'Details': item.Details,
            'Status': int(item.Status)
        }
        address_list.append(address)

    resp['data'] = address_list
    return jsonify(resp)



@route_wechat.route("/editAddress/", methods=['POST'])
def editAdress():
    resp = {'code': 200, 'msg': '添加成功~'}

    Id = request.values['Id'] if 'Id' in request.values else -1

    if Id != -1 and Id:
        # 修改
        summnerNote = Address.query.filter_by(Id=Id).first()
    else:
        # 新增
        summnerNote = Address()

    summnerNote.Cid = request.values['Cid'] if 'Cid' in request.values else ''
    summnerNote.Addressee = request.values['Addressee'] if 'Addressee' in request.values else ''
    summnerNote.AddresseePhone = request.values['AddresseePhone'] if 'AddresseePhone' in request.values else ''
    summnerNote.Province = request.values['Province'] if 'Province' in request.values else ''
    summnerNote.City = request.values['City'] if 'City' in request.values else ''
    summnerNote.County = request.values['County'] if 'County' in request.values else ''
    summnerNote.Details = request.values['Details'] if 'Details' in request.values else ''
    summnerNote.Status = 0

    db.session.add(summnerNote)
    db.session.commit()

    if Id == -1:
        return jsonify(resp)
    else:
        resp['msg']= '修改成功~'
        return jsonify(resp)

@route_wechat.route('/deleteAddress/', methods=['POST'])
def deleteproduct():
    resp = {'code': 200, 'msg': '删除成功'}

    Id = request.values['Id'] if 'Id' in request.values else -1

    result = Address.query.filter_by(Id=Id).first()
    db.session.delete(result)
    db.session.commit()
    return jsonify(resp)


