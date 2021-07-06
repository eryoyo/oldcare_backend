from flask import Blueprint

# 创建蓝图对象
sys_admin = Blueprint("sys_admin", __name__)

from . import api