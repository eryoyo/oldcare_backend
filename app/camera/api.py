import time

from flask import request, session, jsonify, g
from app.camera.camera_collect import camera_collect
from .camera_emotion_identify import camera_emotion_identify
from .camera_fall import camera_fall
from .camera_fence import camera_fence
from .camera_interact import camera_interact
from . import camera


@camera.route("/collect", methods=["POST"])
def pic_collect():
    """
    开始采集视频
    :return:
    """
    get_data = request.get_json()
    path = get_data.get("path")
    print(path)

    time.sleep(60)
    camera_collect(rtsp=path)
    return jsonify(msg="test")


@camera.route("/emotion_identify")
def emotion_identify():
    camera_emotion_identify()
    return jsonify(msg="test")


@camera.route("/fall")
def fall():
    camera_fall()
    return jsonify(msg="test")


@camera.route("/fence")
def fence():
    camera_fence()
    return jsonify(msg="test")


@camera.route("/interact")
def interact():
    camera_interact()
    return jsonify(msg="test")
