from projectCode.user import userFunc, registerApi
from projectCode import db
from projectCode import models
from flask import request
from flask_restful import Resource
from projectCode.utils.common import errorRetult
import re
from projectCode.utils.token_tool import loginValidation
"""编辑蓝图"""


class Register(Resource):
    """注册功能"""

    def get(self):
        return {"status": 200, "messagr": "返回get响应"}

    def post(self):
        """接收post请求,对参数做验证"""
        if request.json:
            """json传参走"""
            name = request.json.get('username')
            pwd = request.json.get('password')
            assertPwd = request.json.get("assertPwd")
            phone = request.json.get('phone')
            email = request.json.get('email')
            address = request.json.get('address')
            role_id = request.json.get("role_name")
            # print(request.json)

        if request.form:
            """form-data传参走"""

            name = request.form['username']
            pwd = request.form['password']
            assertPwd = request.form["assertPwd"]
            phone = request.form['phone']
            email = request.form['email']
            address = request.form['address']
            role_id = request.form["role_name"]
            # print(request.form)

        rePhone = r"^(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\d{8}$"
        reEmail = r"^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$"

        if not all([name, pwd, assertPwd, phone, email, address, role_id]):
            return errorRetult(status=20003)
        if len(name) < 2 or len(name) > 20:
            return errorRetult(status=10011)
        if len(pwd) < 6 or len(pwd) > 16:
            return errorRetult(status=10021)
        if assertPwd != pwd:
            return errorRetult(status=10022)
        if not re.match(rePhone, phone):
            return errorRetult(status=10031)
        if not re.match(reEmail, email):
            return errorRetult(status=10041)
        try:
            dbuser = models.User.query.filter_by(name=name).first()
            if all([dbuser]):
                # 进行用户名重名判断
                return errorRetult(status=10012)
            userInfo = models.User(name=name, password=pwd, phone=phone,
                                   email=email, address=address, role_id=int(role_id))
            db.session.add(userInfo)
            db.session.commit()
            return errorRetult(message="注册成功")
        except Exception as e:
            print(e)
            return errorRetult(status=20002)


registerApi.add_resource(Register, "/register/", endpoint="register")


@userFunc.route("/token/", methods=['get'])
@loginValidation
def TestToken():
    return errorRetult(10000)
