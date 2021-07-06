from flask import request, session, jsonify, g
from app.models import db, Event
from . import camera


@camera.route("/video1", methods=["GET"])
def Video1():
    """
    
    :return:
    """
    pass
