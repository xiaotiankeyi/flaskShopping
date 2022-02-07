import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from projectCode import db
from projectCode import models
from app import app


def innert():
    try:
        with app.app_context():
            goodsify = ['家用电器', '手机', '运营商', '数码', '电脑', '办公', '家具',
                        '家居', '家装', '厨房', '男装', '女装', '童装', '内衣', '美妆',
                        '个性清洁', '宠物', '女鞋', '箱包', '钟表', '珠宝', '男鞋', '运动', '户外']
            for val in goodsify:
                data = models.Goodsify(name=val)
                db.session.add(data)
                db.session.commit()
            return "添加成功"
    except Exception as e:
        print(e)


def select():
    with app.app_context():
        try:
            data = db.session.query(models.Goodsify).get(3)
            return data.retult()
        except Exception as e:
            print(e)

if __name__ == "__main__":
    # innert()
    print(select())
    pass
