import datetime
import math
import json
from flask import request, session, jsonify, g
from app.models import db, OldPerson, to_json
from . import old_person


@old_person.route("/add", methods=["POST"])
def add_old_person():
    """
    {
        "username":"eryo",
        "gender":"女",
        "phone":"15171271104",
        "id_card":"420902200103282044",
        "birthday":"2001-03-28",
        "checkin_date":"2008-09-01",
        "room_number":"room1",
        "guardian_name":"cjl",
        "guardian_phone":"15171271104",
        "guardian_wechat":"cjlwechat"
    }
    增加新的老人
    :return:
    """
    get_data = request.get_json()
    username = get_data.get("username")
    gender = get_data.get("gender")
    phone = get_data.get("phone")
    id_card = get_data.get("id_card")
    birthday = get_data.get("birthday")
    checkin_date = get_data.get("checkin_date")
    room_number = get_data.get("room_number")
    guardian_name = get_data.get("guardian_name")
    guardian_phone = get_data.get("guardian_phone")
    guardian_wechat = get_data.get("guardian_wechat")

    if not all([username, gender, phone, id_card, birthday, checkin_date, room_number, guardian_name, guardian_phone,
                guardian_wechat]):
        return jsonify(msg="参数不全，有缺项", code=4000)

    try:
        old = OldPerson(username=username,
                        gender=gender,
                        phone=phone,
                        id_card=id_card,
                        birthday=birthday,
                        checkin_date=checkin_date,
                        room_number=room_number,
                        guardian_name=guardian_name,
                        guardian_phone=guardian_phone,
                        guardian_wechat=guardian_wechat)
        db.session.add(old)
        db.session.commit()
    except Exception as e:
        print(e)

    id = db.session.execute("select max(id) from old_person").first()

    print(id[0])

    return jsonify(msg="老人" + username + "信息录入成功，老人的编号为" + str(id[0]) + "，请告知老人哟", id=str(id[0]), code=200)


@old_person.route("/modify", methods=["POST"])
def modify_old_person():
    """
    {
        "id":123,
        "username":"eryo",
        "gender":"女",
        "phone":"15171271104",
        "id_card":"420902200103282044",
        "birthday":"2001-03-28",
        "checkin_date":"2008-09-01",
        "room_number":"room1",
        "guardian_name":"cjl",
        "guardian_phone":"15171271104",
        "guardian_wechat":"cjlwechat"
    }
    修改老人信息
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
    room_number = get_data.get("room_number")
    guardian_name = get_data.get("guardian_name")
    guardian_phone = get_data.get("guardian_phone")
    guardian_wechat = get_data.get("guardian_wechat")

    if not all(
            [id, username, gender, phone, id_card, birthday, checkin_date, room_number, guardian_name, guardian_phone,
             guardian_wechat]):
        return jsonify(msg="参数不全，有缺项", code=4000)

    try:
        if OldPerson.query.filter(OldPerson.id == id).count() == 0:
            return jsonify(msg="老人编号不存在哟，请检查之后再进行修改哟！", code=4000)
        OldPerson.query.filter(OldPerson.id == id).update({
            "username": username,
            "gender": gender,
            "phone": phone,
            "id_card": id_card,
            "birthday": birthday,
            "checkin_date": checkin_date,
            "room_number": room_number,
            "guardian_name": guardian_name,
            "guardian_phone": guardian_phone,
            "guardian_wechat": guardian_wechat
        })
        db.session.commit()
    except Exception as e:
        print(e)

    return jsonify(msg="老人" + username + "信息修改成功", code=200)


@old_person.route("/delete", methods=["DELETE"])
def delete_old_person():
    """
    {
        "id":123
    }
    删除老人信息
    :return:
    """
    get_data = request.get_json()
    id = get_data.get("id")

    if not all([id]):
        return jsonify(msg="参数不全，有缺项", code=4000)

    try:
        if OldPerson.query.filter(OldPerson.id == id).count() == 0:
            return jsonify(msg="该老人不存在，检查一下吧！", code=4000)
        OldPerson.query.filter(OldPerson.id == id).delete()
        db.session.commit()
    except Exception as e:
        print(e)

    return jsonify(msg="老人账号注销成功", code=200)


@old_person.route("/checkout", methods=["GET"])
def checkout_old_person():
    """
    {
        "id":123
    }
    老人出养老院
    :return:
    """
    get_data = request.get_json()
    id = get_data.get("id")

    if not all([id]):
        return jsonify(msg="参数不全，有缺项", code=4000)

    try:
        if OldPerson.query.filter(OldPerson.id == id).count() == 0:
            return jsonify(msg="该老人不存在，检查一下吧！", code=4000)
        OldPerson.query.filter(OldPerson.id == id).update({"is_active": 0})
        db.session.commit()
    except Exception as e:
        print(e)

    return jsonify(msg="老人离开养老院手续办理成功", code=200)


@old_person.route("/queryall", methods=["GET"])
def query_all_old_person():
    """
    查询所有老人信息列表
    :return:
    """
    try:
        old_persons = OldPerson.query.all()
        result = to_json(old_persons)
        return jsonify(result)
    except Exception as e:
        print(e)

    return jsonify(msg="test", code=4000)


@old_person.route("/query", methods=["POST"])
def query():
    """
    {
        "id":123
    }
    删除老人信息
    :return:
    """
    get_data = request.get_json()
    id = get_data.get("id")

    if not all([id]):
        return jsonify(msg="参数不全，有缺项", code=4000)

    try:
        if OldPerson.query.filter(OldPerson.id == id).count() == 0:
            return jsonify(msg="该老人不存在，检查一下吧！", code=4000)
        result = OldPerson.query.filter(OldPerson.id == id).first()
        return result.single_to_dict()
    except Exception as e:
        print(e)

    return jsonify(msg="test", code=4001)


@old_person.route("/statistics", methods=["GET"])
def statistics():
    """
    获取老人的统计信息
    :return:
    """
    try:
        d = datetime.date.today()
        today = str(d.year) + '-' + str(d.month) + '-' + str(d.day)
        data = {"1": OldPerson.query.filter(OldPerson.birthday.between('1800-01-01', '1959-12-31')).count(),
                "2": OldPerson.query.filter(OldPerson.birthday.between('1960-01-01', '1969-12-31')).count(),
                "3": OldPerson.query.filter(OldPerson.birthday.between('1970-01-01', '1979-12-31')).count(),
                "4": OldPerson.query.filter(OldPerson.birthday.between('1980-01-01', '1989-12-31')).count(),
                "5": OldPerson.query.filter(OldPerson.birthday.between('1990-01-01', today)).count()}
        return jsonify(msg=json.dumps(data), code=200)
    except Exception as e:
        print(e)

    return jsonify(msg="test", code=4000)


def get_age(birth):
    d = birth.split('-')
    today = datetime.datetime.today()
    bir = datetime.date(year=int(d[0]), month=int(d[1]), day=int(d[2]))
    return math.floor((today - bir).days / 365.0)
