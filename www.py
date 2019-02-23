from application import app

# from web.controllers.index import route_index
from web.controllers.interceptors.apiAuthInterceptor import *
from web.controllers.user.user import route_user
from web.controllers.account import route_account
from web.wechat_controllers import route_wechat
from web.controllers.static import route_static


# app.register_blueprint(route_index, url_prefix="/")
app.register_blueprint(route_static, url_prefix='/api/static')
app.register_blueprint(route_user, url_prefix="/api/user")
app.register_blueprint(route_account, url_prefix="/api/account")
app.register_blueprint(route_wechat, url_prefix="/api/wechat")


