from projectCode.user import userFunc
from projectCode import db
from projectCode import models
from flask import request
from projectCode.utils.common import errorRetult

"""编辑蓝图"""


@userFunc.route("/alterUser/", methods=['post'])
def alterUser():
    """修改用户数据"""
    try:
        id = int(request.form.get('id').strip())
        name = request.form.get('name').strip(
        ) if request.form.get('name') else ''
        pwd = request.form.get('pwd').strip(
        ) if request.form.get('pwd') else ''
        phone = request.form.get('phone').strip(
        ) if request.form.get('phone') else ''
        email = request.form.get('email').strip(
        ) if request.form.get('email') else ''
        address = request.form.get('address').strip(
        ) if request.form.get('address') else ''

        alterdb = models.User.query.get(id)
        if alterdb:
            if name:
                alterdb.name = name
            elif pwd:
                alterdb.password = pwd
            elif phone:
                alterdb.phone = phone
            elif email:
                alterdb.email = email
            elif address:
                alterdb.address = address
            db.session.commit()
            return errorRetult(status=10000, message='数据修改成功')
        else:
            return errorRetult(status=10000, message='查询后无当前用户')
    except Exception as e:
        print(e)
        return errorRetult(20002)
