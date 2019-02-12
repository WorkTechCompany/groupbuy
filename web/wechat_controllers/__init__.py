from flask import Blueprint

route_wechat = Blueprint('wechat', __name__)

from web.wechat_controllers.wechat import *
from web.wechat_controllers.customer import *
from web.wechat_controllers.placeorder import *
from web.wechat_controllers.customer import *
from web.wechat_controllers.personaInformation import *
from web.wechat_controllers.trolley import *

@route_wechat.route('/')
def index():
    return ''
