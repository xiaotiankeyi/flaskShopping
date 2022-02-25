from projectCode import db
from projectCode import models
from projectCode.goodsSystem import goodsSystem
from flask import request
from projectCode.utils.common import errorRetult


@goodsSystem.route("/addgoodsify/", methods=['post'])
def addgoodsify():
    """增加商品种类,通过判断level来实现增加的类型"""
    try:
        name = request.form.get("name")
        level = request.form.get("level")
        parentlevel = request.form.get("parentlevel")

        print(request.form)

        if all([name, level, parentlevel]):
            if level.isdigit() and int(level) == 1:
                data = models.Goodsify(name=name, level=1)

            if level.isdigit() and int(level) == 2:
                data = models.goodsList(name=name, level=2, goodsify_id=int(parentlevel))

            if level.isdigit() and int(level) == 3:
                data = models.Goods(name=name, level=3, goodlist_id=int(parentlevel))

            # db.session.add(data)
            # db.session.commit()
            return errorRetult(10000, message='添加商品种类成功')
        return errorRetult(20000, message='传入数据错误')
    except Exception as e:
        return errorRetult(20000, message=e)


@goodsSystem.route("/findgoodsify/", methods=['get'])
def findgoodsify():
    """获取商品种类"""
    try:
        # 指定查询分类id或是所有
        find = request.args.get("find")
        level = request.args.get("level") if request.args.get("level") else 3

        if level.isdigit:
            """对level进行判断以获取数据的深度"""
            if int(level) in [1, 2, 3]:
                level = level

                if find and find.isdigit():
                    data = db.session.query(models.Goodsify).get(int(find))
                    if data:
                        return errorRetult(10000, message='查询商品种类成功', data=data.retult(int(level)))
                if find and find == "all":
                    data = db.session.query(models.Goodsify).all()
                    if data:
                        return errorRetult(10000, message='查询商品种类成功', data=[val.retult(int(level)) for val in data])
            return errorRetult(20000, message='传入数据错误')
        return errorRetult(20000, message='传入数据错误')
    except Exception as e:
        return errorRetult(20000, message=e)


@goodsSystem.route("/dropgoodsify/", methods=['get'])
def dropgoodsify():
    """删除商品种类"""
    try:
        id = request.args.get("id")

        if all([id]):
            data = db.session.query(models.Goodsify).get(int(id))
            if data:
                db.session.remove(data)
                db.session.commit()
                return errorRetult(10000, message='删除商品种类成功', data=data.retult())
        return errorRetult(20000, message='传入数据错误')
    except Exception as e:
        return errorRetult(20000, message=e)
