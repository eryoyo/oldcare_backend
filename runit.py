from datetime import datetime

from flask_cors import CORS
from flask_socketio import emit

from app import create_app, db, socketio
from flask_script import Manager  # 管理项目的 额外制定一些命令
from flask_migrate import Migrate, MigrateCommand  # 管理数据库需要的脚本 追踪数据库变化的脚本
from concurrent.futures import ThreadPoolExecutor
import time

from app.camera.camera_emotion_identify import camera_emotion_identify
from app.camera.camera_fall import camera_fall
from app.camera.camera_fence import camera_fence
from app.camera.camera_interact import camera_interact

app = create_app("develop")  # 工厂函数模式选择
CORS(app, supports_credentials=True)

# executor = ThreadPoolExecutor(max_workers=5)
# 通过submit函数提交执行的函数到线程池中，submit函数立即返回，不阻塞
# task_emotion = executor.submit(camera_emotion_identify())
# task_fall = executor.submit(camera_fall())
# task_fence = executor.submit(camera_fence())
# task_interact = executor.submit(camera_interact())

name_space = '/dcenter'

@app.route('/push')
def push_once():
    event_name = 'dcenter'
    broadcasted_data = {'data': "test message!"}
    socketio.emit(event_name, broadcasted_data, broadcast=False, namespace=name_space)
    return 'done!'

@socketio.on('connect', namespace=name_space)
def connected_msg():
    print('client connected.')

@socketio.on('disconnect', namespace=name_space)
def disconnect_msg():
    print('client disconnected.')

@socketio.on('my_event', namespace=name_space)
def mtest_message(message):
    print(message)
    emit('my_response',
         {'data': message['data'], 'count': 1})


# manager = Manager(app)  # 用manage进行项目管理 代管app
# Migrate(app, db)  # 把app和db的信息绑定起来进行追踪
#
# manager.add_command("db", MigrateCommand)  # 绑定额外的db命令
# manager.add_command("run", socketio.run(app=app, host="0.0.0.0", port=5001))

if __name__ == '__main__':
    # manager.run()
    app.run(host="0.0.0.0", port=8001, threaded=True)
