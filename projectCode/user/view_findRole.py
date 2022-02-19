from sqlalchemy.orm import query
from projectCode.user import userFunc, registerApi
from projectCode import models
from flask import request
from flask_restful import Resource
from flask_restful import reqparse
from projectCode.utils.common import errorRetult
"""编辑蓝图,处理客户端对用户数据的处理"""


@userFunc.route('/roleInfo/')
def roleInfo():
    """根据id查询单个用户的数据"""
    try:
        id = int(request.args.get("id").strip())
        userdb = models.User.query.filter_by(id=id).first()
        if userdb:
            return errorRetult(status=10000, data=userdb.result_dict())
        else:
            return errorRetult(status=20001, message='查询数据为空')
    except Exception as e:
        print(e)
        return errorRetult(20002)


class UserList(Resource):
    def get(self):
        """
        对用户数据进行分页处理
        query: 查询对象
        pnum: 当前第几页
        pnumsize: 每页/条,显示多少条
        """
        params = reqparse.RequestParser()
        params.add_argument('query', type=str)
        params.add_argument('pnum', type=int)
        params.add_argument('pnumsize', type=int)

        try:
            args = params.parse_args()
            query = args.get('query')
            pnum = args.get('pnum') if args.get('pnum') else 1
            pnumsize = args.get('pnumsize') if args.get('pnum') else 3

            if query:
                """实现模糊查询"""
                userdb = models.User.query.filter(
                    models.User.name.like(f'%{query}%')).paginate(pnum, pnumsize)
            else:
                """实现分页查询"""
                userdb = models.User.query.paginate(pnum, pnumsize)
            userDB = {
                'pnum': pnum,
                'totapage': userdb.total,
                'userlist': [u.result_dict() for u in userdb.items]
            }
            return errorRetult(status=10000, data=userDB)
        except Exception as e:
            return errorRetult(20002)


registerApi.add_resource(UserList, '/user_list/')
