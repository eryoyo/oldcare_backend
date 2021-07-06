from flask import Blueprint

# 创建蓝图对象
event = Blueprint("event", __name__)

from . import api