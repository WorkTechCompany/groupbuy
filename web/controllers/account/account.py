from flask import request, redirect , jsonify
from web.controllers.account import route_account
from common.libs.Helper import ops_render, iPagination, getCurrentDate
from common.libs.user.UserService import UserService
from common.models.User import User
from sqlalchemy import or_
from application import app, db

# 管理员
@route_account.route("/user/")
def user():
    resq = {}
    req = request.values
    query = User.query
    page = int(req['p']) if ('p' in req and req['p']) else 1

    if 'mix_kw' in req:
        rule = or_(User.nickname.ilike("%{0}%".format(req['mix_kw'])), User.mobile.ilike("%{0}%".format(req['mix_kw'])))
        query = query.filter(rule)

    if 'status' in req and int(req['status']) > -1:
        query = query.filter(User.status == int(req['status']))

    count = query.count()
    page_params = {
        'total': count,
        'page_size': app.config['PAGE_SIZE'],
        'page': page,
        'display': app.config['PAGE_DISPLAY'],
        'url': request.full_path.replace("&p={}".format(page), "")
    }
    pages = iPagination(page_params)
    offset =  (page - 1) * app.config['PAGE_SIZE']
    limit = app.config['PAGE_SIZE'] * page
    list = query.order_by(User.uid.desc()).all()[offset: limit]
    resq['list'] = list
    resq['pages'] = pages
    resq['search_con'] = req
    resq['status_mapping'] = app.config['STATUS_MAPPING']
    return ops_render("account/index.html", resq)


@route_account.route("/set/", methods= ["GET","POST"])
def set():
    default_pwd = "********"

    if request.method =="GET":
        resp_data = {}
        req = request.args
        uid = int(req.get("id", 0))

        user_info =None
        if uid:
            user_info = User.query.filter_by(uid = uid).first()

        resp_data['info'] = user_info

        return ops_render("account/set.html", resp_data)


    resp = {'code': 200 , 'msg': '操作成功', 'data': {}}
    req = request.values

    id = req['id'] if 'id' in req else ''
    nickname = req['nickname'] if 'nickname' in req else ''
    mobile = req['mobile'] if 'mobile' in req else ''
    email = req['email'] if 'email' in req else ''
    login_name = req['login_name'] if 'login_name' in req else ''
    login_pwd = req['login_pwd'] if 'login_pwd' in req else ''
    identity = req['identity'] if 'identity' in req else ''

    if nickname is None or len(nickname) < 1:
        resp['code'] = -1
        resp['msg'] = '昵称填写不正确'
        return jsonify(resp)

    if mobile is None or len(mobile) < 1:
        resp['code'] = -1
        resp['msg'] = '手机填写不正确'
        return jsonify(resp)

    if email is None or len(email) < 1:
        resp['code'] = -1
        resp['msg'] = '邮箱填写不正确'
        return jsonify(resp)

    if login_name is None or len(login_name) < 1:
        resp['code'] = -1
        resp['msg'] = '登录名填写不正确'
        return jsonify(resp)

    if login_pwd is None or len(login_pwd) < 1:
        resp['code'] = -1
        resp['msg'] = '密码填写不正确'
        return jsonify(resp)

    has_in = User.query.filter(User.login_name == login_name, User.uid != id).first()
    if has_in:
        resp['code'] = -1
        resp['msg'] = '登录名已存在'
        return jsonify(resp)

    user_info = User.query.filter_by(uid=id).first()
    if user_info:
        model_user = user_info
    else:
        model_user = User()
        model_user.login_salt = UserService.geneSalt()

    model_user.nickname = nickname
    model_user.mobile = mobile
    model_user.email = email
    model_user.login_name = login_name
    model_user.identity = identity
    if default_pwd != login_pwd:
        model_user.login_pwd = UserService.genePwd(login_pwd, model_user.login_salt)

    model_user.updated_time = getCurrentDate()
    model_user.created_time = getCurrentDate()

    db.session.add(model_user)
    db.session.commit()

    return jsonify(resp)


@route_account.route("/ops", methods=["POST"])
def ops():
    resp = {
        'code': 200,
        'msg':'操作成功',
        'data': {}
    }

    req = request.values
    id = req['id'] if 'id' in req else ''
    act = req['act'] if 'act' in req else ''

    if not id:
        resp['code'] = -1
        resp['msg'] = "操作失败1"
        return jsonify(resp)

    if act not in ['remove', 'recover']:
        resp['act'] = -1
        resp['act'] = "操作失败2"
        return jsonify(resp)

    user_info = User.query.filter_by(uid=id).first()

    if not user_info:
        resp['code'] = -1
        resp['msg'] = "操作失败3"

    if act == "remove":
        user_info.status = 0
    elif act == "recover":
        user_info.status = 1

    user_info.updated_time = getCurrentDate()
    db.session.add(user_info)
    db.session.commit()

    return jsonify(resp)