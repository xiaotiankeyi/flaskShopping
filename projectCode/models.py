from datetime import datetime
from msilib import Table
from pickle import TRUE
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

    # 查看谁关联我
    # roles = db.relationship('Role', secondary=roleMenu)

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
        # menuslist = []
        # if self.menus:
        #     for val in self.menus:
        #         if val.Level == 1:
        #             frist_dict = val.get_subLevel()
        #             menuslist.append(frist_dict[0])
        #         if val.Level == 2:
        #             pass
        #     return menuslist
        # return menuslist
        menuslist = []
        if self.menus:
            for val in self.menus:
                if val.Level == 1:
                    frist_dict = val.result_dict()

                    frist_dict['subLevel'] = []
                    # 重新对所有menus循环,查找出属于上个val的下级
                    for i in self.menus:
                        if i.Level == 2 and i.parentLevel == val.id:
                            frist_dict['subLevel'].append(i.get_subLevel())
                    menuslist.append(frist_dict)
        return menuslist
