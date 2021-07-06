from flask import Blueprint

# 创建蓝图对象
volunteer = Blueprint("volunteer", __name__)

from . import api