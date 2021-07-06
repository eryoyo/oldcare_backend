import redis
from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from config import config_map, redis_store
from flask_mail import Mail

import pymysql

db = SQLAlchemy()
mail = Mail()


def create_app(dev_name):
    """
    返回一个实例化并且配置好数据的一个app
    dev_name：选择环境的参数
    :return:
    """
    app = Flask(__name__)
    config_class = config_map.get(dev_name)
    app.config.from_object(config_class)  # 从类中读取需要的信息

    db.init_app(app)  # 实例化的数据库 配置信息

    mail.init_app(app)  # 实例化的邮箱 配置信息

    # 利用flask-session，将session数据保存到redis中
    Session(app)

    # 注册蓝图
    from app import event  # 导入包
    from app import old_person
    from app import staff
    from app import sys_admin
    from app import volunteer
    from app import camera

    app.register_blueprint(event.event, url_prefix="/event")  # 绑定包里面的蓝图对象
    app.register_blueprint(old_person.old_person, url_prefix="/old_person")
    app.register_blueprint(staff.staff, url_prefix="/staff")
    app.register_blueprint(sys_admin.sys_admin, url_prefix="/sys_admin")
    app.register_blueprint(volunteer.volunteer, url_prefix="/volunteer")
    app.register_blueprint(camera.camera, url_prefix="/camera")
    return app
