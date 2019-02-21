APP = {
    'domain': 'https://www.17bctech.com'
}

UPLOAD = {
    'ext': ['jpg', 'gif', 'bmp', 'jpeg', 'png'],
    'prefix_path': '/web/static/upload/',
    'prefix_url': '/static/upload/'
}

AUTH_COOKIE_NAME = 'UserCookie'
SERVER_PORT = '5050'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://bryant:leekobe24@cd-cdb-nmj4h99o.sql.tencentcdb.com:63625/groupbuy'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ENCODING = "utf8mb4"
SQLALCHEMY_BINDS = {
    'groupbuy': "mysql+pymysql://bryant:leekobe24@cd-cdb-nmj4h99o.sql.tencentcdb.com:63625/groupbuy"
}

API_IGNORE_URLS = [
    "^/account"
]

IGNORE_CHECK_LOGIN_URLS = [
    "^/static"
]

## 过滤url
IGNORE_URLS = [
    "^/user/login"
    # "^/upload"

]

MINA_APP = {
    'appid':'wx1f244139ab0c54c8',
    # 'appid': 'wx67efb8952b1c941c',
    'appkey':'c7435a2f34d9f774144696fa68648499',
    # 'appkey': '8723974ba43eb0d3f0405d2bdf2db38f',
    'paykey': 'TM8KwVFRlp0hsTWMQTxLplfFIzmk7csr',
    'mch_id': '1513434041',
    # 'mch_id': '1471175702',
    'callback_url': '/account/callback/'
}

PAY_STATUS_DISPLAY_MAPPING = {
    "0":"订单关闭",
    "1":"支付成功",
    "-8":"待支付",
    "-7":"待发货",
    "-6":"待确认",
    "-5":"待评价"
}