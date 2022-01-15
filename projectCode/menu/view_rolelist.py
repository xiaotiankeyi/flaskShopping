from projectCode.menu import menuApi
from flask_restful import Resource
from projectCode import models
from projectCode.utils.common import errorRetult
from flask import request
from projectCode import db


class autoRoleList(Resource):
    def get(self):
        """查询角色"""
        try:
            if request.form:
                id = request.form.get("id")
                allData = models.Role.query.get(id)
                alldatalist = []
                alldatalist.append(allData.result_dict())
                return errorRetult(status=10000, data=alldatalist)

            allData = models.Role.query.all()
            alldatalist = []
            for i in allData:
                alldatalist.append(i.result_dict())
            return errorRetult(status=10000, data=alldatalist)
        except Exception as e:
            return errorRetult(status=20002)
    pass

    def post(self):
        """ 注册角色"""
        try:
            name = request.form.get("username")
            info = request.form.get("info")

            if name:
                print(name, info)
                allData = models.Role(name=name, desc=info)
                db.session.add(allData)
                db.session.commit()

                return errorRetult(status=10000, message='用户添加成功')
        except Exception as e:
            return errorRetult(status=20002, data=e)

    def delete(self):
        """删除角色"""
        try:
            id = int(request.args.get("id").strip())

            if id:
                data = models.Role.query.get(id)
                db.session.delete(data)
                db.session.commit()

                return errorRetult(10000, message='删除用户成功')
        except Exception as e:
            return errorRetult(20002)

    def put(self):
        """修改角色"""
        try:
            id = request.form.get("id")
            name = request.form.get("username")
            info = request.form.get("info")

            data = models.Role.query.get(int(id))
            if data:
                if name:
                    data.name = name.strip()
                if info:
                    data.info = info.strip()
                db.session.commit()
                return errorRetult(10000, message='修改成功')
            return errorRetult(20002, message="所修改用户不存在")
        except Exception as e:
            return errorRetult(20002, data=e)


menuApi.add_resource(autoRoleList, "/rolelist/")
