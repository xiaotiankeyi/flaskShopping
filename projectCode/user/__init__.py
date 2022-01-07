from flask import Blueprint
from flask_restful import Api

"""创建蓝图对象"""
userFunc = Blueprint("userFunc", __name__, url_prefix="/user")
registerApi = Api(userFunc)


"""引用视图,让视图起作用"""
from projectCode.user import view_user
