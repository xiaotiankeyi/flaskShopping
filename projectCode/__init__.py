from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import configDict

db = SQLAlchemy()


def create(config_Key):
    """初始化app"""
    app = Flask(__name__)

    # 加载配置对象
    configObj = configDict.get(config_Key)
    app.config.from_object(configObj)

    # 防止在把app传回来,在这先绑定app对象
    db.init_app(app=app)

    """蓝图注册必须是app对象和db对象创建后初始化完成后才注册"""
    from projectCode.user import userFunc
    app.register_blueprint(userFunc)

    from projectCode.menu import menuFunc
    app.register_blueprint(menuFunc)

    from projectCode.goodsSystem import goodsSystem
    app.register_blueprint(goodsSystem)

    @app.route('/')
    def hello_world():
        return 'Hello World!'

    return app


if __name__ == '__main__':
    # app.run()
    pass
