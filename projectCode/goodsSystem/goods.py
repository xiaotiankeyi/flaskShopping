from multiprocessing import cpu_count
from time import process_time_ns
from traceback import print_tb
from projectCode import db
from projectCode import models
from projectCode.goodsSystem import goodsSystem
from flask import request
from projectCode.utils.common import errorRetult
from flask import current_app
from werkzeug.utils import secure_filename


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


@goodsSystem.route("/uploadPictrue", methods=['post'])
def uploadPictrue():
    fileObj = request.files.get('file')

    if judgePictrue(fileObj.filename):
        pictruePath = current_app.config['SERVER_IMG_UPLOADS']

        file = secure_filename(fileObj.filename)
        # print(file)

        fileObj.save(f"{pictruePath}\\{file}")
        # http://127.0.0.1:5000/static/img/phone.jpg

        data = {
            'path': f'/static/img/{file}',
            'url': f'/static/img/{file}'
        }
        return errorRetult(10000, message='上传成功', data=data)

    else:
        return errorRetult(20000, message='上传失败')


def judgePictrue(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in current_app.config['ALLOWED_IMG']
