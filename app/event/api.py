import datetime

from flask import request, session, jsonify, g, render_template
from app.models import db, Event_emotion, Event_falldown, Event_forbid, Event_interact, Event_interrupt, to_json
from . import event
from threading import Lock
from app import socketio

thread = None
thread_lock = Lock()


def send_to_front(msg):
    event_name = 'dcenter'
    broadcasted_data = {'data': msg, 'time': str(datetime.datetime.now())}
    socketio.emit(event_name, broadcasted_data, broadcast=False, namespace="/dcenter")
    print('完成一条消息的发送')


@event.route('/')
def index():
    return "woooooooo"


@event.route('/emotion')
def query_emotion():
    """
        查询所有老人笑的信息列表
        :return:
        """
    try:
        events = Event_emotion.query.all()
        result = to_json(events)
        return jsonify(result)
    except Exception as e:
        print(e)

    return jsonify(msg="test", code=4000)


def insert_emotion(type, old_person_id):
    try:
        event_emotion = Event_emotion(type=type,
                                      old_person_id=old_person_id)
        db.session.add(event_emotion)
        db.session.commit()
    except Exception as e:
        print(e)


@event.route('/interrupt')
def query_interrupt():
    """
        查询所有陌生人闯入的信息列表
        :return:
        """
    try:
        events = Event_interrupt.query.all()
        result = to_json(events)
        return jsonify(result)
    except Exception as e:
        print(e)

    return jsonify(msg="test", code=4000)


def insert_interrupt():
    try:
        event_interrupt = Event_interrupt()
        db.session.add(event_interrupt)
        db.session.commit()
    except Exception as e:
        print(e)


@event.route('/interact')
def query_interact():
    """
        查询所有义工交互的信息列表
        :return:
        """
    try:
        events = Event_interact.query.all()
        result = to_json(events)
        return jsonify(result)
    except Exception as e:
        print(e)

    return jsonify(msg="test", code=4000)


def insert_interact(old_person_id, volunteer_id):
    try:
        event_interact = Event_interact(old_person_id=old_person_id,
                                        volunteer_id=volunteer_id)
        db.session.add(event_interact)
        db.session.commit()
    except Exception as e:
        print(e)


@event.route('/forbid')
def query_forbid():
    """
        查询所有闯入禁区的信息列表
        :return:
        """
    try:
        events = Event_forbid.query.all()
        result = to_json(events)
        return jsonify(result)
    except Exception as e:
        print(e)

    return jsonify(msg="test", code=4000)


def insert_forbid():
    try:
        event_forbid = Event_forbid()
        db.session.add(event_forbid)
        db.session.commit()
    except Exception as e:
        print(e)


@event.route('/falldown')
def query_falldown():
    """
        查询所有摔倒的信息列表
        :return:
        """
    try:
        events = Event_falldown.query.all()
        result = to_json(events)
        return jsonify(result)
    except Exception as e:
        print(e)

    return jsonify(msg="test", code=4000)


def insert_falldown():
    try:
        event_falldown = Event_falldown()
        db.session.add(event_falldown)
        db.session.commit()
    except Exception as e:
        print(e)