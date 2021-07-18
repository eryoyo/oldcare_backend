from app import db
from datetime import datetime


# 事件表-老人笑了事件发生
class Event_emotion(db.Model):
    __tablename__ = "event_emotion"
    id = db.Column(db.Integer, primary_key=True)  # 事件id
    type = db.Column(db.String(50))  # 表情
    event_date = db.Column(db.DateTime, default=datetime.now)  # 事件发生时间-插入的时间，精确到秒，下一次插入的时间间隔需要超过2分钟
    event_location = db.Column(db.String(200), default="房间")  # 事件发生地点-确定为房间
    old_person_id = db.Column(db.Integer, db.ForeignKey('old_person.id'))  # 老人id

    # 单个对象方法1
    def to_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        return model_dict

    # 单个对象方法2
    def single_to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    # 多个对象
    def dobule_to_dict(self):
        result = {}
        for key in self.__mapper__.c.keys():
            if getattr(self, key) is not None:
                result[key] = str(getattr(self, key))
            else:
                result[key] = getattr(self, key)
        return result


# 事件表-陌生人闯入事件
class Event_interrupt(db.Model):
    __tablename__ = "event_interrupt"
    id = db.Column(db.Integer, primary_key=True)  # 事件id
    event_date = db.Column(db.DateTime, default=datetime.now)  # 事件发生时间
    event_location = db.Column(db.String(200), default="房间")  # 事件发生地点-确定为房间

    # 单个对象方法1
    def to_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        return model_dict

    # 单个对象方法2
    def single_to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    # 多个对象
    def dobule_to_dict(self):
        result = {}
        for key in self.__mapper__.c.keys():
            if getattr(self, key) is not None:
                result[key] = str(getattr(self, key))
            else:
                result[key] = getattr(self, key)
        return result


# 事件表-义工交互检测
class Event_interact(db.Model):
    __tablename__ = "event_interact"
    id = db.Column(db.Integer, primary_key=True)  # 事件id
    event_date = db.Column(db.DateTime, default=datetime.now)  # 事件发生时间
    event_location = db.Column(db.String(200), default="活动室")  # 事件发生地点-确定为活动室
    old_person_id = db.Column(db.Integer, db.ForeignKey('old_person.id'))
    volunteer_id = db.Column(db.Integer, db.ForeignKey('volunteer.id'))

    # 单个对象方法1
    def to_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        return model_dict

    # 单个对象方法2
    def single_to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    # 多个对象
    def dobule_to_dict(self):
        result = {}
        for key in self.__mapper__.c.keys():
            if getattr(self, key) is not None:
                result[key] = str(getattr(self, key))
            else:
                result[key] = getattr(self, key)
        return result


# 事件表-摔倒
class Event_falldown(db.Model):
    __tablename__ = "event_falldown"
    id = db.Column(db.Integer, primary_key=True)  # 事件id
    event_date = db.Column(db.DateTime, default=datetime.now)  # 事件发生时间
    event_location = db.Column(db.String(200), default="走廊")  # 事件发生地点-确定为走廊

    # 单个对象方法1
    def to_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        return model_dict

    # 单个对象方法2
    def single_to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    # 多个对象
    def dobule_to_dict(self):
        result = {}
        for key in self.__mapper__.c.keys():
            if getattr(self, key) is not None:
                result[key] = str(getattr(self, key))
            else:
                result[key] = getattr(self, key)
        return result


# 事件表-进入禁区
class Event_forbid(db.Model):
    __tablename__ = "event_forbid"
    id = db.Column(db.Integer, primary_key=True)  # 事件id
    event_date = db.Column(db.DateTime, default=datetime.now)  # 事件发生时间
    event_location = db.Column(db.String(200), default="院子")  # 事件发生地点-确定为院子

    # 单个对象方法1
    def to_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        return model_dict

    # 单个对象方法2
    def single_to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    # 多个对象
    def dobule_to_dict(self):
        result = {}
        for key in self.__mapper__.c.keys():
            if getattr(self, key) is not None:
                result[key] = str(getattr(self, key))
            else:
                result[key] = getattr(self, key)
        return result


# 事件表
# class Event(db.Model):
#     __tablename__ = "event"
#     id = db.Column(db.Integer, primary_key=True)  # 事件id
#     # 0：情感检测      地点（房间）、时间、老人
#     # 1：义工交互检测  地点（桌子）、时间、义工、老人
#     # 2：陌生人检测   地点（房间）、时间
#     # 3：摔倒检测    地点（走廊）、时间
#     # 4：禁止区     地点（院子）、时间
#     event_type = db.Column(db.Integer)  # 事件类型
#     event_date = db.Column(db.DateTime)  # 事件发生时间
#     event_location = db.Column(db.String(200))  # 事件发生地点
#     event_desc = db.Column(db.String(200))  # 事件描述
#     is_handled = db.Column(db.Integer, nullable=False, default=1)
#     old_person_id = db.Column(db.Integer, db.ForeignKey('old_person.id'))
#
#     # 单个对象方法1
#     def to_dict(self):
#         model_dict = dict(self.__dict__)
#         del model_dict['_sa_instance_state']
#         return model_dict
#
#     # 单个对象方法2
#     def single_to_dict(self):
#         return {c.name: getattr(self, c.name) for c in self.__table__.columns}
#
#     # 多个对象
#     def dobule_to_dict(self):
#         result = {}
#         for key in self.__mapper__.c.keys():
#             if getattr(self, key) is not None:
#                 result[key] = str(getattr(self, key))
#             else:
#                 result[key] = getattr(self, key)
#         return result


class OpenID(db.Model):
    __tablename__ = "open_id"
    id = db.Column(db.Integer, primary_key=True)  # open_id的编号
    username = db.Column(db.String(50))  # open_id的具体内容


# 老人表
class OldPerson(db.Model):
    __tablename__ = "old_person"
    id = db.Column(db.Integer, primary_key=True)  # 老人id
    username = db.Column(db.String(50))  # 老人姓名
    gender = db.Column(db.String(5))  # 性别
    phone = db.Column(db.String(50))  # 电话号码
    id_card = db.Column(db.String(50))  # 身份证号
    birthday = db.Column(db.DateTime)  # 出生日期
    checkin_date = db.Column(db.DateTime)  # 入养老院日期
    checkout_date = db.Column(db.DateTime)  # 离开养老院日期
    imgset_dir = db.Column(db.String(200))  # 图像路径
    profile_photo = db.Column(db.String(200))  # 头像路径
    room_number = db.Column(db.String(50))  # 房间号
    guardian_name = db.Column(db.String(50))  # 监护人姓名
    guardian_phone = db.Column(db.String(50))  # 监护人电话
    guardian_wechat = db.Column(db.String(50))  # 监护人微信
    # 是否仍在养老院
    is_active = db.Column(db.Integer, nullable=False, default=1)
    event_emotion = db.relationship("Event_emotion", backref="old_person")  # 关联事件
    event_interact = db.relationship("Event_interact", backref="old_person")  # 关联事件

    # 单个对象方法1
    def to_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        return model_dict

    # 单个对象方法2
    def single_to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    # 多个对象
    def dobule_to_dict(self):
        result = {}
        for key in self.__mapper__.c.keys():
            if getattr(self, key) is not None:
                result[key] = str(getattr(self, key))
            else:
                result[key] = getattr(self, key)
        return result


# 工作人员表
class Staff(db.Model):
    __tablename__ = "staff"
    id = db.Column(db.Integer, primary_key=True)  # 工作人员id
    username = db.Column(db.String(50))  # 工作人员姓名
    gender = db.Column(db.String(5))  # 性别
    phone = db.Column(db.String(50))  # 电话号码
    id_card = db.Column(db.String(50))  # 身份证号
    birthday = db.Column(db.DateTime)  # 出生日期
    hire_date = db.Column(db.DateTime)  # 入职养老院日期
    resign_date = db.Column(db.DateTime)  # 离开养老院日期
    imgset_dir = db.Column(db.String(200))  # 图像路径
    profile_photo = db.Column(db.String(200))  # 头像路径
    # 是否仍在养老院
    is_active = db.Column(db.Integer, nullable=False, default=1)

    # 单个对象方法1
    def to_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        return model_dict

    # 单个对象方法2
    def single_to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    # 多个对象
    def dobule_to_dict(self):
        result = {}
        for key in self.__mapper__.c.keys():
            if getattr(self, key) is not None:
                result[key] = str(getattr(self, key))
            else:
                result[key] = getattr(self, key)
        return result


# 系统管理员表
class SysAdmin(db.Model):
    __tablename__ = "sys_admin"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    real_name = db.Column(db.String(50))
    sex = db.Column(db.String(20))
    email = db.Column(db.String(50))
    phone = db.Column(db.String(50))
    # open_id = db.Column(db.String(50))      # 微信的号
    is_active = db.Column(db.Integer, nullable=False, default=1)

    # 单个对象方法1
    def to_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        return model_dict

    # 单个对象方法2
    def single_to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    # 多个对象
    def dobule_to_dict(self):
        result = {}
        for key in self.__mapper__.c.keys():
            if getattr(self, key) is not None:
                result[key] = str(getattr(self, key))
            else:
                result[key] = getattr(self, key)
        return result

# 义工表
class Volunteer(db.Model):
    __tablename__ = "volunteer"
    id = db.Column(db.Integer, primary_key=True)  # 义工id
    username = db.Column(db.String(50))  # 姓名
    gender = db.Column(db.String(5))  # 性别
    phone = db.Column(db.String(50))  # 电话号码
    id_card = db.Column(db.String(50))  # 身份证号
    birthday = db.Column(db.DateTime)  # 出生日期
    checkin_date = db.Column(db.DateTime)  # 入养老院日期
    checkout_date = db.Column(db.DateTime)  # 离开养老院日期
    imgset_dir = db.Column(db.String(200))  # 图像路径
    profile_photo = db.Column(db.String(200))  # 头像路径
    # 是否仍在养老院
    is_active = db.Column(db.Integer, nullable=False, default=1)
    event_interact = db.relationship("Event_interact", backref="volunteer")  # 关联事件

    # 单个对象方法1
    def to_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        return model_dict

    # 单个对象方法2
    def single_to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    # 多个对象
    def dobule_to_dict(self):
        result = {}
        for key in self.__mapper__.c.keys():
            if getattr(self, key) is not None:
                result[key] = str(getattr(self, key))
            else:
                result[key] = getattr(self, key)
        return result


# 配合多个对象使用的函数
def to_json(all_vendors):
    v = [ven.dobule_to_dict() for ven in all_vendors]
    return v
