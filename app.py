from projectCode import create, db
from flask_migrate import Migrate

"""
三种配置模式
    "development"
    "production"
    "test"
"""

app = create("development")

"""执行前先导入模型"""
Migrate(app=app, db=db)

if __name__ == "__main__":
    app.run()
