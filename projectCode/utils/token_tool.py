"""
生成token方式,
1、加密数据
2、加密算法
3、秘钥
"""


from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, request
from projectCode.models import User
from projectCode.utils.common import errorRetult


def createAutnToken(IDvalue, timeValidity):
    """生成token,IDvalue用户id,timeValidity有效期"""
    condingObj = Serializer(
        current_app.config['SECRET_KEY'], timeValidity)

    return condingObj.dumps({"id": IDvalue}).decode()


def decodeAutnToken(tokenValue):
    """解码用户传送过来的token"""
    decodeObj = Serializer(current_app.config['SECRET_KEY'])

    try:
        obj = decodeObj.loads(tokenValue)
    except Exception:
        return None
    user = User.query.filter_by(id=obj['id']).first()
    return user


def loginValidation(viewFunc):
    """对token有效性进行验证"""
    def tokenValidation(*args, **kwargs):
        try:
            tokenVal = request.headers["token"]
        except Exception:
            return errorRetult(30000)

        decodeObj = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = decodeObj.loads(tokenVal)
        except Exception:
            return errorRetult(30001)
        return viewFunc(*args, **kwargs)

    return tokenValidation
