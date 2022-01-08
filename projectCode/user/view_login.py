from sqlalchemy.orm import query
from projectCode.user import userFunc
from projectCode import models
from flask import request

from projectCode.utils.common import errorRetult
from projectCode.utils.token_tool import createAutnToken
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
