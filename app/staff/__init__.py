from flask import Blueprint

# 创建蓝图对象
staff = Blueprint("staff", __name__)

from . import api