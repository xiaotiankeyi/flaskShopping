from projectCode.user import userFunc
from projectCode import db
from projectCode import models
from flask import request
from projectCode.utils.common import errorRetult
import re
"""编辑蓝图,put请求会自动转为json数据格式"""


@userFunc.route("/alterUser/", methods=['put'])
def alterUser():
    """修改用户数据"""
    try:
        if request.json:
            print('json', request.json)

            id = int(request.json.get('id'))
            phone = request.json.get('phone').strip()
            email = request.json.get('email').strip()
            address = request.json.get('address').strip()
            role_id = request.json.get("role_name")

        alterdb = models.User.query.get(id)

        rePhone = r"^(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\d{8}$"
        reEmail = r"^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$"

        if alterdb:
            if not re.match(rePhone, phone):
                return errorRetult(20002)
            if not re.match(reEmail, email):
                return errorRetult(20002)
            if all([role_id]):
                alterdb.role_id = int(role_id)

            alterdb.email = email
            alterdb.phone = phone
            alterdb.address = address
            db.session.commit()
            return errorRetult(status=10000, message='数据修改成功')
        else:
            return errorRetult(status=10000, message='查询后无当前用户')
    except Exception as e:
        print(e)
        return errorRetult(20002)
