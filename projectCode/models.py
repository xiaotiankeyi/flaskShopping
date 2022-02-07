from datetime import datetime
from email.policy import default
from typing_extensions import Self
from sqlalchemy.orm import backref

from werkzeug.security import generate_password_hash, check_password_hash

from projectCode import db


class BaseModel():
    """表基础字段"""
    createTime = db.Column(db.DATETIME, default=datetime.now)
    """onupdate=datetime.now实现字段变更后就实时更新"""
    updateTime = db.Column(
        db.DATETIME, default=datetime.now, onupdate=datetime.now)


class User(db.Model, BaseModel):
    __tablename__ = "t_user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    pwd = db.Column(db.String(250))
    phone = db.Column(db.String(11))
    email = db.Column(db.String(32))
    address = db.Column(db.String(32))

    # 建立和角色的一对多关系
    role_id = db.Column(db.Integer, db.ForeignKey('t_role.id'))

    """模型中密码的优化处理"""

    @property
    def password(self):
        return self.pwd

    @password.setter
    def password(self, pwd_v):
        """generate_password_hash对密码进行加密"""
        self.pwd = generate_password_hash(pwd_v)

    def check_password(self, pwd_v):
        """用户登录后,进行和加密后的密码进行对照"""
        return check_password_hash(self.pwd, pwd_v)

    def result_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "address": self.address,
            "role_name": self.role.name if self.role else None
        }


# 创建菜单列表和role的多对多关系
roleMenu = db.Table(
    't_rolemenu',
    db.Column('id', db.Integer, primary_key=True, autoincrement=True),
    db.Column('role_id', db.Integer, db.ForeignKey(
        't_role.id'), primary_key=True),
    db.Column('menu_id', db.Integer, db.ForeignKey(
        't_meun.id'), primary_key=True)
)


class Menu(db.Model):
    __tablename__ = "t_meun"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    Level = db.Column(db.Integer)
    parentLevel = db.Column(db.Integer, db.ForeignKey('t_meun.id'))
    path = db.Column(db.String(32))

    # 自关联
    subLevel = db.relationship("Menu")

    def result_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "Level": self.Level,
            "parentLevel": self.parentLevel,
            "path": self.path,
        }

    def get_subLevel(self):
        for val in self.subLevel:
            return val.result_dict()
        return self.result_dict()


class Role(db.Model):
    __tablename__ = "t_role"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    desc = db.Column(db.String(32))

    user = db.relationship('User', backref='role')
    # 角色查看相关菜单
    menus = db.relationship('Menu', secondary=roleMenu)

    def result_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "desc": self.desc,
            "menus": self.getMenulit()
        }

    def getMenulit(self):
        menuslist = []

        if self.menus:
            menus = sorted(self.menus, key=lambda x: x.id, reverse=False)
            for val in menus:
                if val.Level == 1:
                    frist_dict = val.result_dict()

                    frist_dict['subLevel'] = []
                    # 重新对所有menus循环,查找出属于上个val的下级
                    for i in menus:
                        if i.Level == 2 and i.parentLevel == val.id:
                            frist_dict['subLevel'].append(i.get_subLevel())
                    menuslist.append(frist_dict)
        return menuslist


class Goodsify(db.Model):
    """商品分类模型"""
    __tablename__ = "t_goodsify"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    level = db.Column(db.Integer, default=1)

    goodsObj = db.relationship('goodsList', backref=db.backref('goodsify'))

    def retult(self, level=3):
        return {
            "id": self.id,
            "name": self.name,
            "level": self.level,
            "child_node": self.goodslistdata(level)
        }

    def goodslistdata(self, level):
        """获取子节点数据, 根据前端返回回去层级"""

        datalist = []
        if level == 3:
            goodsdata = self.goodsObj
            if goodsdata:
                for val in goodsdata:
                    datalist.append(val.retult())
                return datalist
            return datalist
        if level == 2:
            goodsdata = self.goodsObj
            if goodsdata:
                for val in goodsdata:
                    datalist.append(val.now_retult())
                return datalist
            return datalist

        if level == 1:
            return datalist


class goodsList(db.Model):
    """商品详细品种"""
    __tablename__ = "t_goodslist"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    level = db.Column(db.Integer)

    goodsify_id = db.Column(db.Integer, db.ForeignKey('t_goodsify.id'))

    goods = db.relationship('Goods', backref=db.backref('goodslist'))

    def retult(self):
        """获取当前成和下一层"""
        return {
            "id": self.id,
            "name": self.name,
            "level": self.level,
            "goodsify_id": self.goodsify_id,
            "child_node": self.goodsdata()
        }

    def goodsdata(self):
        """获取子节点数据"""
        datalist = []
        goodsdata = self.goods
        if goodsdata:
            for val in goodsdata:
                datalist.append(val.retult())
            return datalist
        return datalist

    def now_retult(self):
        """只获取当前"""
        return {
            "id": self.id,
            "name": self.name,
            "level": self.level,
            "goodsify_id": self.goodsify_id,
        }


class Goods(db.Model):
    """具体商品"""
    __tablename__ = "t_goods"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), nullable=False)
    level = db.Column(db.Integer)

    goodlist_id = db.Column(db.Integer, db.ForeignKey('t_goodslist.id'))

    def retult(self):
        return {
            "id": self.id,
            "name": self.name,
            "level": self.level,
            "goodlist_id": self.goodlist_id
        }
