from flask import Blueprint

route_account = Blueprint("account", __name__)

from web.controllers.account.shop import *
from web.controllers.account.product import *
from web.controllers.account.shop import *
from web.controllers.account.utils import *
from web.controllers.account.apply import *
from web.controllers.account.customer import *


@route_account.route('/')
def index():
    return ''