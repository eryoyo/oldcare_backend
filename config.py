import redis
redis_store = redis.Redis(host='127.0.0.1', port=6379, db=1)


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "sdfsdfsdf"
    # flask-session配置
    SESSION_TYPE = "redis"
    SESSION_USE_SIGNER = True  # 对cookie中session_id进行隐藏处理 加密混淆
    PERMANENT_SESSION_LIFETIME = 1800  # session数据的有效期，单位秒
    # 邮箱配置
    MAIL_SERVER = "smtp.qq.com"
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = "xxx@qq.com"
    MAIL_PASSWORD = "xxx"


# 开发环境
class DevelopmentConfig(Config):
    """开发模式的配置信息"""
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/oldcare'
    SESSION_REDIS = redis.Redis(host='127.0.0.1', port=6379, password="123456", db=2)  # 操作的redis配置
    # DEBUG = True


# 线上环境
class ProductionConfig(Config):
    """生产环境配置信息"""
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/oldcare'
    SESSION_REDIS = redis.Redis(host='127.0.0.1', port=6379, password="123456", db=3)  # 操作的redis配置


config_map = {
    "develop": DevelopmentConfig,
    "product": ProductionConfig
}