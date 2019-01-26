from flask import Blueprint


route_account = Blueprint("account", __name__)

from web.controllers.account.shop import *
from web.controllers.account.product import *
from web.controllers.account.shop import *
from web.controllers.account.utils import *
from web.controllers.account.apply import *


@route_account.route('/')
def index():
    return ''