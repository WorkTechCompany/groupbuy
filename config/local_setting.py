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
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:aaaaaaaa@localhost:3306/groupbuy'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ENCODING = "utf8mb4"
SQLALCHEMY_BINDS = {
    'groupbuy': "mysql+pymysql://root:aaaaaaaa@localhost:3306/groupbuy"
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
    'appkey':'c7435a2f34d9f774144696fa68648499',
    'paykey':'TM8KwVFRlp0hsTWMQTxLplfFIzmk7csr',
    'mch_id':'1513434041',
    'callback_url':'/account/callback/'
}

PAY_STATUS_DISPLAY_MAPPING = {
    "0":"订单关闭",
    "1":"支付成功",
    "-8":"待支付",
    "-7":"待发货",
    "-6":"待确认",
    "-5":"待评价"
}