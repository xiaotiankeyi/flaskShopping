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
from datetime import datetime, timedelta


def tokenTime():
    '''设置token有效期5分钟'''
    ToTime = (datetime.now() + timedelta(minutes=5)
              ).strftime("%Y-%m-%d %H:%M:%S")

    nowTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    ToTime = datetime.strptime(ToTime, "%Y-%m-%d %H:%M:%S")
    nowTime = datetime.strptime(nowTime, "%Y-%m-%d %H:%M:%S")

    lastTime = (ToTime - nowTime).total_seconds()
    return int(lastTime)


def createAutnToken(IDvalue, timeValidity=tokenTime):
    """生成token,IDvalue用户id,timeValidity有效期"""
    condingObj = Serializer(
        current_app.config['SECRET_KEY'], timeValidity)

    return condingObj.dumps({"id": str(IDvalue)}).decode()


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
    """每请求一个请求都需要对token有效性进行验证"""
    def tokenValidation(*args, **kwargs):
        try:
            tokenVal = request.headers["token"]
        except Exception:
            # 没有接收到token,返回30000
            return errorRetult(30000)

        decodeObj = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = decodeObj.loads(tokenVal)
        except Exception:
            # 对token进行解析,错误就返回30001
            return errorRetult(30001)
        return viewFunc(*args, **kwargs)

    return tokenValidation
