from web.wechat_controllers import route_wechat
from common.libs.user.UserService import UserService
from common.libs.Helper import getCurrentDate
from common.models.apply import Apply, db
from application import app, db
from flask import request, jsonify
from common.models.customer import Customer
from common.models.customer_login import CustomerLogin


# 用户信息
# 注册
@route_wechat.route("/customeSignin/", methods=['POST'])
def customesignin():
    default_pwd = "********"

    resp = {'code': 200, 'msg': '注册成功'}
    CustomerPhone = request.values['CustomerPhone'] if 'CustomerPhone' in request.values else -1

    check = CustomerLogin.query.filter_by(CustomerPhone=CustomerPhone).first()
    if check:
        resp['code'] = -1
        resp['msg'] = '手机号已注册'
        return jsonify(resp)

    CustomerPassword = request.values['CustomerPassword'] if 'CustomerPassword' in request.values else -1
    CustomerPayword = request.values['CustomerPayword'] if 'CustomerPayword' in request.values else -1

    signup = CustomerLogin()

    signup.CustomerPhone = CustomerPhone

    signup.Password_salt = UserService.geneSalt()
    if default_pwd != CustomerPassword:
        signup.CustomerPassword = UserService.genePwd(CustomerPassword, signup.Password_salt)

    signup.Payword_salt = UserService.geneSalt()
    if default_pwd != CustomerPassword:
        signup.CustomerPayword = UserService.genePwd(CustomerPayword, signup.Payword_salt)

    signup.created_time = getCurrentDate()
    Cid = signup.Cid
    db.session.add(signup)
    db.session.commit()

    addinfo = Customer()

    addinfo.Cid = Cid
    addinfo.CustomerName = request.values['CustomerName'] if 'CustomerName' in request.values else '未知名字'
    addinfo.CustomerPhone = CustomerPhone
    addinfo.MyBalance = float('%.2f' % 0)
    addinfo.AvailableBalance = float('%.2f' % 0)
    addinfo.MyIncome = float('%.2f' % 0)
    addinfo.Cidentity = 1
    db.session.add(addinfo)
    db.session.commit()

    return jsonify(resp)

@route_wechat.route("/customeLogin/", methods=['POST'])
def customeLogin():
    result = {'code': 200, 'msg': '登录成功'}
    req = request.values
    CustomerPhone = req['CustomerPhone'] if 'CustomerPhone' in req else ''
    CustomerPassword = req['CustomerPassword'] if 'CustomerPassword' in req else ''

    if CustomerPhone is None or len(CustomerPhone) < 1:
        result['code'] = -1
        result['msg'] = 'error'
        response = jsonify(result)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    if CustomerPassword is None or len(CustomerPassword) < 1:
        result['code'] = -1
        result['msg'] = 'error'
        response = jsonify(result)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    user_info = CustomerLogin.query.filter_by(CustomerPhone=CustomerPhone).first()

    if not user_info:
        result['code'] = -1
        result['msg'] = '账号错误'
        response = jsonify(result)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    if user_info.CustomerPassword != UserService.genePwd(CustomerPassword, user_info.Password_salt):
        result['code'] = -1
        result['msg'] = '密码错误'
        response = jsonify(result)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    # response = make_response(json.dumps(result))
    # response.headers['Access-Control-Allow-Origin'] = '*'
    # response.set_cookie(app.config['AUTH_COOKIE_NAME'], "%s#%s" % (UserService.geneAuthCode(user_info), user_info.uid))
    result['Cid'] = user_info.Cid
    return jsonify(result)

# 用户余额
@route_wechat.route("/CustomerInfo/", methods=['GET', 'POST'])
def customerinfo():

    resp = {'code': 200, 'msg': '查询成功'}
    req = request.values
    Cid = req['Cid'] if 'Cid' in request.values else -1
    if Cid == -1:
        resp['code'] = -1
        resp['msg'] = '账户异常'
        response = jsonify(resp)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    info = Customer.query.filter_by(Cid=Cid).first()
    resp['info'] = {
        'Cid': Cid,
        'CustomerName': info.CustomerName,
        'CustomerPhone': info.CustomerPhone,
        'MyBalance': str(info.MyBalance),
        'AvailableBalance': str(info.AvailableBalance),
        "MyIncome": str(info.MyIncome)
    }
    return jsonify(resp)





