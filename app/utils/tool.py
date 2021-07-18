import functools
import random

from flask import session, jsonify, g
from flask_sqlalchemy import SQLAlchemy

from app import mail, create_app
from flask_mail import Message

# 定义的验证登录状态的装饰器
from app.models import OpenID
from app.wechat.api import send_event


def admin_login_required(view_func):
    # # wraps函数的作用是将wrapper内层函数的属性设置为被装饰函数view_func的属性
    @functools.wraps(view_func)
    def wrapper(*args, **kwargs):
        # 判断用户的登录状态
        id = session.get("id")

        # 如果用户是登录的， 执行视图函数
        if id is not None:
            # 将user_id保存到g对象中，在视图函数中可以通过g对象获取保存数据
            g.id = id
            return view_func(*args, **kwargs)
        else:
            # 如果未登录，返回未登录的信息
            return jsonify(code=400, msg="用户未登录")

    return wrapper


# 发送邮件
def send_mail(mail_subject, mail_recipients, mail_body):
    # with app.app_context():
    msg = Message(mail_subject, sender="2226006725@qq.com",
                  recipients=mail_recipients)
    msg.body = mail_body
    mail.send(msg)
    print("已发送一封邮件到" + str(mail_recipients))


# 生成随机验证码
def random_code(n=6, alpha=True):
    """
    生成随机验证码
    :param n: 验证码的位数
    :param alpha: 验证码中是否含有字母
    :return: 验证码
    """
    s = ''  # 创建字符串变量,存储生成的验证码
    for i in range(n):  # 通过for循环控制验证码位数
        num = random.randint(0, 9)  # 生成随机数字0-9
        if alpha:  # 需要字母验证码,不用传参,如果不需要字母的,关键字alpha=False
            upper_alpha = chr(random.randint(65, 90))
            lower_alpha = chr(random.randint(97, 122))
            num = random.choice([num, upper_alpha, lower_alpha])
        s = s + str(num)
    return s


# def add_open_id(open_id):
#     app2 = create_app("develop")
#     db2 = SQLAlchemy(app2)
#     with app2.app_context():
#         try:
#             open = OpenID(username=open_id)
#             db2.session.add(open)
#             db2.session.commit()
#         except Exception as e:
#             print(e)


# def send_to_all(msg):
#     """
#     发送微信消息给所有系统管理员
#     :return:
#     """
#     send_event("ooVV56IKYPX8ff4xzYCfYI3EO5Ng", msg)
#     # app2 = create_app("develop")
#     # with app2.app_context():
#     #     try:
#     #         open_ids = OpenID.query.all()
#     #         for i in open_ids:
#     #             send_event(i.username, msg)
#     #     except Exception as e:
#     #         print(e)