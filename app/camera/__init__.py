from flask import Blueprint

# 创建蓝图对象
camera = Blueprint("camera", __name__)

from . import api
