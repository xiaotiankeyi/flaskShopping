from projectCode.user import userFunc
from projectCode import db
from projectCode import models
from flask import request
from projectCode.utils.common import errorRetult
"""编辑蓝图,put请求会自动转为json数据格式"""


@userFunc.route("/alterPassword/", methods=['put'])
def alterPassword():
    """修改用户数据"""
    try:
        id = request.form.get('id')
        chonfiyPwd = request.form.get('assertPwd')
        print(request.form)

        alterdb = models.User.query.get(id)
        if alterdb:
            if len(chonfiyPwd) < 6 or len(chonfiyPwd) > 16:
                return errorRetult(20002, message='密码格式不合法')
            alterdb.password = chonfiyPwd
            db.session.commit()
            return errorRetult(status=10000, message='修改密码成功')
        else:
            return errorRetult(status=10000, message='查询后无当前用户')
    except Exception as e:
        print(e)
        return errorRetult(20002)
