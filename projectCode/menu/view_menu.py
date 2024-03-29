from projectCode import db
from projectCode import models
from flask import request
from flask_restful import Resource

from projectCode.menu import menuApi
from projectCode.utils.common import errorRetult


class MenuHandle(Resource):
    def get(self):
        type_ = request.args.get("type")
        menuList = []
        if type_ == "list":
            dataMenu = models.Menu.query.filter(models.Menu.Level != 0).all()
            for val in dataMenu:
                menuList.append(val.result_dict())
        else:
            dataMenu = models.Menu.query.filter(models.Menu.Level == 1).all()
            for val in dataMenu:
                # 一级数据转json
                jsonData = val.result_dict()

                if val.subLevel:
                    # 有下级菜单就,在一级数据基础上添加二级数据容器
                    jsonData['subLevel'] = []

                    # 循环一级数据下的二级数据
                    for res in val.subLevel:
                        # 二级数据转json
                        TwojsonData = res.result_dict()

                        # 在往一级数据里添加二级数据
                        jsonData['subLevel'].append(TwojsonData)

                menuList.append(jsonData)

        return errorRetult(status=1000, data=menuList)


menuApi.add_resource(MenuHandle, '/menulist/')
