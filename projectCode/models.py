from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from projectCode import db


class BaseModel():
    """表基础字段"""
    createTime = db.Column(db.DATETIME, default=datetime.now)
    """onupdate=datetime.now实现字段变更后就实时更新"""
    updateTime = db.Column(db.DATETIME, default=datetime.now, onupdate=datetime.now)


class User(db.Model, BaseModel):
    __tablename__ = "t_user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    pwd = db.Column(db.String(250))
    phone = db.Column(db.String(11))
    email = db.Column(db.String(32))
    address = db.Column(db.String(32))

    """模型中密码的优化处理"""

    @property
    def password(self):
        return self.pwd

    @password.setter
    def password(self, pwd_v):
        """generate_password_hash对密码进行加密"""
        self.pwd = generate_password_hash(pwd_v)

    def check_password(self, pwd_v):
        """用户登录后,进行和加密后的密码进行对照"""
        return check_password_hash(self.pwd, pwd_v)
