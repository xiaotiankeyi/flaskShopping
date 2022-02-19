from projectCode import db
from projectCode import models
from projectCode.goodsSystem import goodsSystem
from flask import request
from projectCode.utils.common import errorRetult


@goodsSystem.route('/alterGoods/', methods=['post'])
def alterGoods():
    # 修改商品描述
    id = request.form.get('id')
    info = request.form.get('info')

    if id and id.isdigit():
        data = db.session.query(models.Goods).get(int(id))
        if data:
            data.info = info.split()
            db.session.commit()
            return errorRetult(message='修改成功')
        return errorRetult(status=2000, message='无数据')
    return errorRetult(status=2000, message='数据转入错误')


@goodsSystem.route("/dropgoods/", methods=['get'])
def dropgoods():
    """删除商品种类"""
    try:
        id = request.args.get("id")

        if all([id]):
            data = db.session.query(models.Goods).get(int(id))
            if data:
                db.session.remove(data)
                db.session.commit()
                return errorRetult(10000, message='删除商品成功', data=data.retult())
        return errorRetult(20000, message='传入数据错误')
    except Exception as e:
        return errorRetult(20000, message=e)


@goodsSystem.route("/findgoods/", methods=['get'])
def findgoods():
    # 查找商品
    try:
        id = request.args.get('id')

        if all([id]):
            # 通过指定id查询
            data = db.session.query(models.Goods).get(int(id))

        return errorRetult(status=10000, data=data.retult(), message="查询成功")

    except Exception as e:
        return errorRetult(status=20000, message=e)


@goodsSystem.route("/findgoodsPaging/", methods=['get'])
def findgoodsPaging():
    # 实现分页查询
    try:
        query = request.args.get('query')
        pnum = request.args.get("pnum")
        pnumsize = request.args.get("pnumsize")

        if all([query]):
            # 模糊搜索
            data = db.session.query(models.Goods).filter(
                models.Goods.name.like(f'%{query}%')).paginate(int(pnum), int(pnumsize))
        else:
            # 分页操作
            data = db.session.query(models.Goods).filter_by().paginate(
                page=int(pnum), per_page=int(pnumsize))

        goodsDB = {
            'pnum': pnum,
            'totapage': data.total,
            'goodslist': [u.retult() for u in data.items]
        }
        return errorRetult(status=10000, data=goodsDB, message="查询成功")
    except Exception as e:
        return errorRetult(status=20000, message="查找失败")
