from flask import Blueprint, request, jsonify, make_response
from common.libs.Helper import ops_render
from common.models.User import User
from application import app, db
from common.libs.user.UserService import UserService
from web.controllers.user import route_user
import json

@route_user.route("/login/", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return ops_render("user/login.html")

    result = {'code': 200, 'msg': '操作成功'}
    req = request.values
    login_name = req['login_name'] if 'login_name' in req else ''
    login_pwd = req['login_pwd'] if 'login_pwd' in req else ''

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

    user_info = User.query.filter_by(login_name=login_name).first()
    if not user_info:
        result['code'] = -1
        result['msg'] = '账号错误'
        response = jsonify(result)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

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

    result['identity'] = user_info.identity
    result['Aid'] = user_info.Aid

    response = make_response(json.dumps(result))
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.set_cookie(app.config['AUTH_COOKIE_NAME'], "%s#%s" % (UserService.geneAuthCode(user_info), user_info.uid))


    return response


@route_user.route("/checkdeploy/", methods=["GET","POST"])
def checkdeploy():
    return 'success'