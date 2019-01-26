from application import db


class User(db.Model):
    __tablename__ = 'user'

    uid = db.Column(db.BigInteger, primary_key=True)                                                        # 用户uid
    nickname = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())                  # 用户名
    mobile = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())                     # 手机号码
    email = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())                     # 邮箱地址
    login_name = db.Column(db.String(20), nullable=False, unique=True, server_default=db.FetchedValue())    # 登录用户名
    login_pwd = db.Column(db.String(32), nullable=False, server_default=db.FetchedValue())                  # 登录密码
    login_salt = db.Column(db.String(32), nullable=False, server_default=db.FetchedValue())                 # 登录密码的随机加密秘钥
    identity = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())                      # 身份
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())                        # 1：有效 0：无效
