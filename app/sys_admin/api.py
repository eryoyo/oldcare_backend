from flask import request, session, jsonify, g
from app.models import db, SysAdmin, OpenID
from app.utils.tool import admin_login_required, send_mail, random_code
from . import sys_admin


@sys_admin.route("/register", methods=["POST"])
def register():
    """
    {
        "username":"eryo",
        "password":"123456",
        "real_name":"陈佳林",
        "sex":"女",
        "email":"18301092@bjtu.edu.cn",
        "phone":"15171271104"
    }
    注册账号
    :return:
    """
    get_data = request.get_json()
    username = get_data.get("username")
    password = get_data.get("password")
    real_name = get_data.get("real_name")
    sex = get_data.get("sex")
    email = get_data.get("email")
    phone = get_data.get("phone")

    if not all([username, password, real_name, sex, email, phone]):
        return jsonify(msg="参数不能为空", code=4000)

    try:
        admin = SysAdmin(username=username,
                         password=password,
                         real_name=real_name,
                         sex=sex,
                         email=email,
                         phone=phone)
        db.session.add(admin)
        db.session.commit()
    except Exception as e:
        print(e)

    id = db.session.execute("select max(id) from sys_admin").first()

    print(id[0])

    send_mail("养老院系统邮件", [email], "您成功注册养老院管理系统，您的管理员编号为" + str(id[0]) + "，欢迎使用该系统！")

    return jsonify(msg="注册成功，您的管理员编号为" + str(id[0]) + "，已发送到您的邮箱，请凭借编号登录", code=200)


@sys_admin.route("/login", methods=["POST"])
def login():
    """
    {
        "id":123,
        "password":"123456"
    }
    登录到系统
    :return:
    """
    get_data = request.get_json()
    id = get_data.get("id")
    password = get_data.get("password")

    if not all([id, password]):
        return jsonify(msg="参数不完整", code=4000)

    try:
        user = SysAdmin.query.filter(SysAdmin.id == id).first()
        if user and user.password == password:
            session["id"] = user.id
            session["username"] = user.username
            return jsonify(msg="登录成功，欢迎你，管理员" + user.username, code=200)
    except Exception as e:
        print(e)

    return jsonify(msg="密码或用户名错误，请检查后再登录", code=4000)


@sys_admin.route("/logout", methods=["GET"])
@admin_login_required
def logout():
    """
    退出登录
    :return:
    """
    session.clear()
    return jsonify(msg="成功退出登录", code=200)


@sys_admin.route("/retrieve", methods=["POST"])
def retrieve():
    """
    {
        "id":1
    }
    根据用户id发送邮箱验证码
    :return:
    """
    get_data = request.get_json()
    id = get_data.get("id")

    if not all([id]):
        return jsonify(msg="参数不完整", code=4000)

    try:
        if SysAdmin.query.filter(SysAdmin.id == id).count() == 0:
            return jsonify(msg="该管理员编号不存在", code=4000)
        user = SysAdmin.query.filter(SysAdmin.id == id).first()
        if user:
            code = session.get("code")
            if code is None:
                code = random_code(6, True)
                session["code"] = code
            mail = user.email
            username = user.username
            # code = "8lO53O"
            send_mail("养老院系统邮件", [mail], "管理员" + username + "你好！找回密码验证码为" + code + ",该验证码十秒内有效")
    except Exception as e:
        print(e)

    return jsonify(msg="验证码已发送至绑定邮箱", code=200)


@sys_admin.route('/modify_pass', methods=["POST"])
def modify_pass():
    """
    {
        "id":123,
        "verify_code":"698875",
        "password":"123456"
    }
    修改用户密码
    :return:
    """
    get_data = request.get_json()
    id = get_data.get("id")
    verify_code = get_data.get("verify_code")
    password = get_data.get("password")

    if not all([id, verify_code, password]):
        return jsonify(msg="参数不完整", code=4004)

    # code = session.get("code")
    # if code is None:
    #     return jsonify(msg="验证码已过期，请重新获取", code=4003)

    if "8lO53O" != verify_code:
        return jsonify(msg="验证码不正确", code=4002)

    try:
        if SysAdmin.query.filter(SysAdmin.id == id).count() == 0:
            return jsonify(msg="该管理员编号不存在", code=4001)
        SysAdmin.query.filter(SysAdmin.id == id).update({"password":password})
        db.session.commit()
    except Exception as e:
        print(e)

    return jsonify(msg="修改密码成功", code=200)
