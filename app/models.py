from . import db
from datetime import datetime


# 时间表
class Event(db.Model):
    __tablename__ = "event"
    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.Integer)
    event_date = db.Column(db.DateTime)
    event_location = db.Column(db.String(200))
    event_desc = db.Column(db.String(200))
    is_handled = db.Column(db.Integer, nullable=False, default=1)
    old_person_id = db.Column(db.Integer, db.ForeignKey('old_person.id'))

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


# 老人表
class OldPerson(db.Model):
    __tablename__ = "old_person"
    id = db.Column(db.Integer, primary_key=True) # 老人id
    username = db.Column(db.String(50))     # 老人姓名
    gender = db.Column(db.String(5))        # 性别
    phone = db.Column(db.String(50))        # 电话号码
    id_card = db.Column(db.String(50))      # 身份证号
    birthday = db.Column(db.DateTime)       # 出生日期
    checkin_date = db.Column(db.DateTime)   # 入养老院日期
    checkout_date = db.Column(db.DateTime)  # 离开养老院日期
    imgset_dir = db.Column(db.String(200))  # 图像路径
    profile_photo = db.Column(db.String(200))   # 头像路径
    room_number = db.Column(db.String(50))      # 房间号
    guardian_name = db.Column(db.String(50))    # 监护人姓名
    guardian_phone = db.Column(db.String(50))   # 监护人电话
    guardian_wechat = db.Column(db.String(50))  # 监护人微信
    # 是否仍在养老院
    is_active = db.Column(db.Integer, nullable=False, default=1)
    events = db.relationship("Event", backref="old_person")  # 关联事件

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
    v = [ ven.dobule_to_dict() for ven in all_vendors ]
    return v