# from application import app
# from flask import request, g, jsonify, redirect
# from common.libs.UrlManager import UrlManager
# from common.models.apply import Apply
# from common.models.User import User
# from common.libs.member.UserService import UserService
# import re
#
# '''
# account认证
# '''
#
#
# @app.before_request
# def before_request_api():
#     ignore_urls = app.config['IGNORE_URLS']
#     ignore_check_login_urls = app.config['IGNORE_CHECK_LOGIN_URLS']
#     path = request.path
#     print(path)
#
#     # 如果是静态文件就不要查询用户信息了
#     pattern = re.compile('%s' % "|".join(ignore_check_login_urls))
#     if pattern.match(path):
#         return
#
#     if '/account' not in path:
#         return
#
#     pattern = re.compile('%s' % "|".join(ignore_urls))
#     if pattern.match(path):
#         return
#
#     member_info = check_member_login()
#     g.member_info = None
#     if member_info:
#         g.member_info = member_info
#
#     pattern = re.compile('%s' % "|".join(ignore_urls))
#     if pattern.match(path):
#         return
#
#     if not member_info :
#         resp = {'code': 2000, 'msg': '未登录~', 'data': {}}
#         return jsonify(resp)
#
#     return
#
# '''
# 判断用户是否已经登录
# '''
#
#
# def check_member_login():
#     try:
#         auth_cookie = request.values['Authorization']
#     except Exception:
#         return False
#
#     if auth_cookie is None:
#         return False
#
#     auth_info = auth_cookie.split("#")
#     if len(auth_info) != 3:
#         return False
#
#     try:
#         if auth_info[0] == '1':
#             member_info = User.query.filter_by(uid=auth_info[2]).first()
#         else:
#             member_info = Apply.query.filter_by(Aid=auth_info[2]).first()
#     except Exception:
#         return False
#
#     if member_info is None:
#         return False
#
#     if auth_info[0] == '1':
#         if auth_info[1] != UserService.geneAuthCode(member_info):
#             return False
#     else:
#         if auth_info[1] != UserService.geneAidCode(member_info):
#             return False
#
#
#     return member_info
