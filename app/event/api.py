from flask import request, session, jsonify, g
from app.models import db, Event
from . import event
from runit import app
from app import mail
from flask_mail import Message


@event.route("/test", methods=["GET"])
def test():
    #with app.app_context():
    msg = Message("测试", sender="2226006725@qq.com",
                  recipients=["18301092@bjtu.edu.cn"])
    msg.body = "这是一个邮件内容"
    mail.send(msg)
    print("已发送一封邮件")
    return "woooooo"
