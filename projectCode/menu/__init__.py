from flask import Blueprint
from flask_restful import Api

"""创建蓝图对象"""
menuFunc = Blueprint("menuFunc", __name__, url_prefix="/menu")
menuApi = Api(menuFunc)


"""引用视图,让视图起作用"""
from projectCode.menu.view_menu import MenuHandle
from projectCode.menu import view_rolelist