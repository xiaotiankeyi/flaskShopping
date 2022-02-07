from projectCode.menu import menuApi, menuFunc
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


@menuFunc.route("/delauto/")
def delAuto():
    """实现角色权限的删除"""
    try:
        role_id = int(request.form.get("Rid"))
        menu_id = int(request.form.get("Mid"))

        roleObj = models.Role.query.get(role_id)
        menuObj = models.Menu.query.get(menu_id)

        if all([roleObj, menuObj]):
            if menuObj in roleObj.menus:
                roleObj.menus.remove(menuObj)

                # 删除根目录时把下级目录也删除
                if menuObj.Level == 1:
                    for i in menuObj.subLevel:
                        # 判断当前下级目录在角色menus中
                        if i in roleObj.menus:
                            roleObj.menus.remove(i)
                db.session.commit()
                return errorRetult(10000, message="删除权限成功")
            return errorRetult(20000, message="当前用户没有该权限")
        return errorRetult(20000, message="传递数据有误")
    except Exception as e:
        print(e)
        return errorRetult(20000, message=e)


@menuFunc.route("/addauto/", methods=['post'])
def addAuto():
    """实现角色权限的增加"""
    try:
        role_id = int(request.form.get("Rid"))
        menu_id = int(request.form.get("Mid"))

        roleObj = models.Role.query.get(role_id)
        menuObj = models.Menu.query.get(menu_id)

        if all([roleObj, menuObj]):
            # 先判断权限是不是一级权限
            if menuObj.Level == 1:
                roleObj.menus.append(menuObj)
            else:
                # 获取二级权限的父权限一起添加
                parentID = menuObj.parentLevel
                parentLevel = models.Menu.query.get(parentID)
                roleObj.menus.append(parentLevel)
                roleObj.menus.append(menuObj)

            db.session.commit()
            return errorRetult(10000, message="添加权限成功")

        return errorRetult(20000, message="参数传递错误")
    except Exception as e:
        print(e)
        return errorRetult(20000, message=e)
