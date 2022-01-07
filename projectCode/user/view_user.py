from sqlalchemy.orm import query
from projectCode.user import userFunc, registerApi
from projectCode import db
from projectCode import models
from flask import request
from flask_restful import Resource
from flask_restful import reqparse
from projectCode.utils.common import errorRetult
import re
from projectCode.utils.token_tool import createAutnToken, loginValidation
"""编辑蓝图"""


@userFunc.route("/login/", methods=['POST'])
def login():
    """实现登录"""
    name = request.form["username"]
    pwd = request.form['password']

    # name = request.form.get("username")
    # pwd = request.form.get('password')
    # print(name, pwd)

    if not all([name, pwd]):
        return {"status": 10000, "message": "数据不完整"}
    if len(name) > 1:
        user = models.User.query.filter_by(name=name).first()
        if user:
            if user.check_password(pwd):
                token = createAutnToken(IDvalue=user.id)
                return errorRetult(message="登录成功", data={"token": token})
    return errorRetult(status=20001)


class Register(Resource):
    """注册功能"""

    def get(self):
        return {"status": 200, "messagr": "返回get响应"}

    def post(self):
        """接收post请求,对参数做验证"""
        name = request.form['username']
        pwd = request.form['password']
        assertPwd = request.form["assertPwd"]
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']

        rePhone = r"^(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\d{8}$"
        reEmail = r"^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$"

        if not all([name, pwd, phone, email, address]):
            return errorRetult(status=20003)
        if len(name) < 2:
            return errorRetult(status=10011)
        if len(pwd) < 6:
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
                                   email=email, address=address)
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


@userFunc.route('/roleInfo/')
def roleInfo():
    try:
        id = int(request.args.get("id").strip())
        userdb = models.User.query.filter_by(id=id).first()
        if userdb:
            return errorRetult(status=10000, data=userdb.__repr__())
        else:
            return errorRetult(status=20001, message='查询数据为空')
    except Exception as e:
        print(e)
        return errorRetult(20002)


class UserList(Resource):
    def get(self):
        """
        query: 查询对象
        pnum: 当前第几页
        pnumsize: 一页多少数量
        """
        params = reqparse.RequestParser()
        params.add_argument('query', type=str)
        params.add_argument('pnum', type=int)
        params.add_argument('pnumsize', type=int)

        try:
            args = params.parse_args()
            query = args.get('query')
            pnum = args.get('pnum') if args.get('pnum') else 1
            pnumsize = args.get('pnumsize') if args.get('pnum') else 2
            if query:
                userdb = models.User.query.filter(
                    models.User.name.like(f'%{query}%')).paginate(pnum, pnumsize)
            else:
                userdb = models.User.query.paginate(pnum, pnumsize)
            userDB = {
                'pnum': pnum,
                'totapage': userdb.total,
                'userlist': [u.__repr__() for u in userdb.items]
            }
            return errorRetult(status=10000, data=userDB)
        except Exception as e:
            return errorRetult(20002)


registerApi.add_resource(UserList, '/user_list/')