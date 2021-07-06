from flask import request, session, jsonify, g
from app.models import db, Staff, to_json
from . import staff


@staff.route("/add", methods=["POST"])
def add_staff():
    """
    {
        "username":"eryo",
        "gender":"女",
        "phone":"15171271104",
        "id_card":"420902200103282044",
        "birthday":"2001-03-28",
        "checkin_date":"2008-09-01"
    }
    增加新的工作人员
    :return:
    """
    get_data = request.get_json()
    username = get_data.get("username")
    gender = get_data.get("gender")
    phone = get_data.get("phone")
    id_card = get_data.get("id_card")
    birthday = get_data.get("birthday")
    checkin_date = get_data.get("checkin_date")

    if not all([username, gender, phone, id_card, birthday, checkin_date]):
        return jsonify(msg="参数不全，有缺项", code=4000)

    try:
        sta = Staff(username=username,
                    gender=gender,
                    phone=phone,
                    id_card=id_card,
                    birthday=birthday,
                    hire_date=checkin_date)
        db.session.add(sta)
        db.session.commit()
    except Exception as e:
        print(e)

    id = db.session.execute("select max(id) from staff").first()

    print(id[0])

    return jsonify(msg="工作人员" + username + "信息录入成功，该工作人员的编号为" + str(id[0]) + "，请告知工作人员哟", code=200)


@staff.route("/modify", methods=["POST"])
def modify_staff():
    """
    {
        "id":123,
        "username":"eryo",
        "gender":"女",
        "phone":"15171271104",
        "id_card":"420902200103282044",
        "birthday":"2001-03-28",
        "checkin_date":"2008-09-01"
    }
    修改工作人员信息
    :return:
    """
    get_data = request.get_json()
    id = get_data.get("id")
    username = get_data.get("username")
    gender = get_data.get("gender")
    phone = get_data.get("phone")
    id_card = get_data.get("id_card")
    birthday = get_data.get("birthday")
    checkin_date = get_data.get("checkin_date")

    if not all([id, username, gender, phone, id_card, birthday, checkin_date]):
        return jsonify(msg="参数不全，有缺项", code=4000)

    try:
        if Staff.query.filter(Staff.id==id).count() == 0:
            return jsonify(msg="工作人员编号不存在，请检查一下哟！", code=4000)
        Staff.query.filter(Staff.id==id).update({
            "username": username,
            "gender": gender,
            "phone": phone,
            "id_card": id_card,
            "birthday": birthday,
            "hire_date": checkin_date
        })
        db.session.commit()
    except Exception as e:
        print(e)

    return jsonify(msg="工作人员" + username + "的信息修改成功", code=200)


@staff.route("/delete", methods=["DELETE"])
def delete_staff():
    """
    {
        "id":123
    }
    删除工作人员
    :return:
    """
    get_data = request.get_json()
    id = get_data.get("id")

    if not all([id]):
        return jsonify(msg="参数不全，有缺项", code=4000)

    try:
        if Staff.query.filter(Staff.id == id).count() == 0:
            return jsonify(msg="该工作人员不存在，检查一下吧！", code=4000)
        Staff.query.filter(Staff.id == id).delete()
        db.session.commit()
    except Exception as e:
        print(e)

    return jsonify(msg="工作人员账号注销成功", code=200)


@staff.route("/checkout", methods=["GET"])
def checkout_staff():
    """
    {
        "id":123
    }
    工作人员离职
    :return:
    """
    get_data = request.get_json()
    id = get_data.get("id")

    if not all([id]):
        return jsonify(msg="参数不全，有缺项", code=4000)

    try:
        if Staff.query.filter(Staff.id == id).count() == 0:
            return jsonify(msg="该工作人员不存在，检查一下吧！", code=4000)
        Staff.query.filter(Staff.id == id).update({"is_active": 0})
        db.session.commit()
    except Exception as e:
        print(e)

    return jsonify(msg="工作人员离开养老院手续办理成功", code=200)


@staff.route("/queryall", methods=["GET"])
def query_all_staff():
    """
    查询全部的工作人员
    :return:
    """
    try:
        staffs = Staff.query.all()
        result = to_json(staffs)
        return jsonify(result)
    except Exception as e:
        print(e)

    return jsonify(msg="test", code=4000)


@staff.route("/statistics", methods=["GET"])
def statistics():
    """
    获取工作人员的统计信息
    :return:
    """
    pass
