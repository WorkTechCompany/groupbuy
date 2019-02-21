from flask import Blueprint

route_account = Blueprint("account", __name__)

from web.controllers.account.shop import *
from web.controllers.account.product import *
from web.controllers.account.shop import *
from web.controllers.account.utils import *
from web.controllers.account.apply import *
from web.controllers.account.customer import *
from web.controllers.account.order import *
from web.controllers.account.balance_log import *


@route_account.route('/')
def index():
    return ''


#                                  _oo8oo_
#                                 o8888888o
#                                 88" . "88
#                                 (| -_- |)
#                                 0\  =  /0
#                               ___/'==='\___
#                             .' \\|     |# '.
#                            / \\|||  :  |||# \
#                           / _||||| -:- |||||_ \
#                          |   | \\\  -  #/ |   |
#                          | \_|  ''\---/''  |_/ |
#                          \  .-\__  '-'  __/-.  /
#                        ___'. .'  /--.--\  '. .'___
#                     ."" '<  '.___\_<|>_/___.'  >' "".
#                    | | :  `- \`.:`\ _ /`:.`/ -`  : | |
#                    \  \ `-.   \_ __\ /__ _/   .-` /  /
#                =====`-.____`.___ \_____/ ___.`____.-`=====
#                                  `=---=`
#
#
#               ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                          强大爷保佑         永不宕机/永无bug