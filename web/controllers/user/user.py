from flask import Blueprint, request, jsonify, make_response
from common.libs.Helper import ops_render
from common.models.User import User
from common.models.shop import Shop
from common.models.apply import Apply
from application import app, db
from common.libs.user.UserService import UserService
from web.controllers.user import route_user
import json

@route_user.route("/login/", methods=["GET","POST"])
def login():

    result = {'code': 200, 'msg': '操作成功'}
    req = request.values
    login_name = req['login_name'] if 'login_name' in req else ''
    login_pwd = req['login_pwd'] if 'login_pwd' in req else ''
    identity = int(req['identity']) if 'identity' in req else -1

    if identity is None:
        result['code'] = -1
        result['msg'] = '请选择身份'
        response = jsonify(result)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    if login_name is None or len(login_name) < 1:
        result['code'] = -1
        result['msg'] = 'error'
        response = jsonify(result)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    if login_pwd is None or len(login_pwd) < 1:
        result['code'] = -1
        result['msg'] = 'error'
        response = jsonify(result)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    if identity == 1:
        user_info = User.query.filter_by(login_name=login_name).first()
    else:
        user_info = Apply.query.filter_by(ApplyPhone=login_name).first()

    if not user_info:
        result['code'] = -1
        result['msg'] = '账号错误'
        response = jsonify(result)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    if identity == 1:
        if user_info.login_pwd != UserService.genePwd(login_pwd, user_info.login_salt):
            result['code'] = -1
            result['msg'] = '密码错误'
            response = jsonify(result)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
        if user_info.status == -1:
            result['code'] = -1
            result['msg'] = '账号失效'
            response = jsonify(result)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
    else:
        if user_info.ApplyPassword != UserService.genePwd(login_pwd, user_info.Applylogin_salt):
            result['code'] = -1
            result['msg'] = '密码错误'
            response = jsonify(result)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response

    if identity == 1:
        result['identity'] = user_info.identity
        result['Authorization'] = UserService.geneAuthCode(user_info)
        result['Shopid'] = 0
    else:
        result['Aid'] = user_info.Aid
        result['Authorization'] = UserService.geneAuthCode_Apply(user_info)
        shop_result = Shop.query.filter_by(Aid=user_info.Aid).first()
        if shop_result:
            result['Shopid'] = shop_result.Shopid
        else:
            result['Shopid'] = -1

    response = make_response(json.dumps(result))
    response.headers['Access-Control-Allow-Origin'] = '*'
    # if identity == 1:
        # response.set_cookie(app.config['AUTH_COOKIE_NAME'], "%s#%s" % (UserService.geneAuthCode(user_info), user_info.uid))
    # else:
    #     response.set_cookie(app.config['AUTH_COOKIE_NAME'], "%s#%s" % (UserService.geneAuthCode(user_info), user_info.Aid))

    return response


@route_user.route("/checkdeploy/", methods=["GET","POST"])
def checkdeploy():
    return 'success'