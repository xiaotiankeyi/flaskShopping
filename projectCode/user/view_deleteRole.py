from projectCode.user import userFunc
from projectCode import db
from projectCode import models
from flask import request
from projectCode.utils.common import errorRetult
"""编辑蓝图"""


@userFunc.route("/deleteUser/", methods=['delete'])
def deleteUser():
    """删除用户数据"""
    try:
        id = int(request.json.get('id'))

        deletedb = models.User.query.get(id)
        if deletedb:
            db.session.delete(deletedb)
            db.session.commit()
            return errorRetult(status=10000, message='数据删除成功')
        else:
            return errorRetult(status=20002, message='查询后无当前用户')
    except Exception as e:
        print(e)
        return errorRetult(20002)
