from web.wechat_controllers import route_wechat
from common.libs.user.UserService import UserService
from common.libs.Helper import getCurrentDate
from common.models.apply import Apply, db
from application import app, db
from flask import request, jsonify
from common.models.customer import Customer
from common.models.customer_login import CustomerLogin
from common.libs.member.MemberService import MemberService


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
    signup.openid = -1
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


# @route_api.route("/member/login", methods=["GET", "POST"])
# def login():
#     resp = {'code': 200, 'msg': "操作成功"}
#     req = request.values
#     code = req['code'] if 'code' in req else ''
#     if not code or len(code) < 1:
#         resp['code'] = -1
#         resp['msg'] = '需要code'
#         return jsonify(resp)
#
#     openid = MemberService.getOpenId(code)
#
#     nickname = req['nickName'] if 'nickName' in req else ''
#     gender = req['gender'] if 'gender' in req else ''
#     avatarUrl = req['avatarUrl'] if 'avatarUrl' in req else ''
#
#     '''
#         判断是否注册过
#     '''
#     bind_info = OauthMemberBind.query.filter_by(openid=openid, type=1).first()
#     if not bind_info:
#         model_member = Member()
#         model_member.nickname = nickname
#         model_member.sex = gender
#         model_member.avatar = avatarUrl
#         model_member.salt = MemberService.geneSalt()
#         model_member.updated_time = getCurrentDate()
#         model_member.created_time = getCurrentDate()
#
#         db.session.add(model_member)
#         db.session.commit()
#
#         model_bind = OauthMemberBind()
#         model_bind.member_id = model_member.id
#         model_bind.type = 1
#         model_bind.openid = openid
#         model_bind.extra = ''
#         model_bind.created_time = getCurrentDate()
#         model_bind.updated_time = getCurrentDate()
#
#         db.session.add(model_bind)
#         db.session.commit()
#
#         bind_info = model_bind
#
#     member_info = Member.query.filter_by(id=bind_info.member_id).first()
#
#     token = "%s#%s" % (MemberService.geneAuthCode(member_info), member_info.id)
#     resp['data'] = {'token': token}
#
#     return jsonify(resp)

@route_wechat.route("/getopenid/", methods=['POST'])
def getopenid():
    result = {'code': 200, 'msg': '获取成功'}
    req = request.values
    code = req['code'] if 'code' in req else ''
    if not code or len(code) < 1:
        result['code'] = -1
        result['msg'] = '需要code'
        return jsonify(result)
    openid = MemberService.getOpenId(code)
    result['openid'] = openid
    return jsonify(result)

@route_wechat.route("/customeLogin/", methods=['POST'])
def customeLogin():
    result = {'code': 200, 'msg': '登录成功'}
    req = request.values
    CustomerPhone = req['CustomerPhone'] if 'CustomerPhone' in req else ''
    CustomerPassword = req['CustomerPassword'] if 'CustomerPassword' in req else ''
    openid = req['openid'] if 'openid' in req else ''
    if not openid or len(openid) < 1:
        result['code'] = -1
        result['msg'] = '需要openid'
        return jsonify(result)

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

    user_info.openid = openid
    db.session.commit()

    token = "%s#%s" % (MemberService.geneAuthCode(user_info), user_info.Cid)
    result['data'] = {'token': token}
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





