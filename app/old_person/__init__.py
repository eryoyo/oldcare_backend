from flask import Blueprint

# 创建蓝图对象
old_person = Blueprint("old_person", __name__)

from . import api