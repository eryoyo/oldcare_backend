import datetime

import cv2
import subprocess
import time

from app.event.api import send_to_front, insert_forbid
# from app.utils.tool import send_to_all
from app.wechat.api import send_event
from model.functions.checkfence import CheckFence
from model.track import CentroidTracker
from imutils.video import FPS


def camera_fence():
    rtsp = "rtmp://192.144.218.105/live/fence_in"
    rtmp = 'rtmp://192.144.218.105/live/fence'

    # starting video streaming
    transportation = {'frame': None, 'status': 0, 'H': None, 'W': None,
                      'intrub': False, 'intrub_time': 0,
                      'ct': CentroidTracker(maxDisappeared=40, maxDistance=50),
                      'trackers': [], 'trackableObjects': {}, 'totalFrames': 0, 'totalDown': 0, 'totalUp': 0,
                      'fps': FPS().start(), 'rgb': None}
    checkFence = CheckFence()
    flag = 0

    # 读取视频并获取属性
    cap = cv2.VideoCapture(rtsp)
    cap.set(0, 640)  # set Width (the first parameter is property_id)
    cap.set(1, 480)  # set Height
    time.sleep(2)
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    sizeStr = str(size[0]) + 'x' + str(size[1])

    command = ['ffmpeg',
               '-y', '-an',
               '-f', 'rawvideo',
               '-vcodec', 'rawvideo',
               '-pix_fmt', 'bgr24',
               '-s', sizeStr,
               '-r', '25',
               '-i', '-',
               '-c:v', 'libx264',
               '-pix_fmt', 'yuv420p',
               '-preset', 'ultrafast',
               '-f', 'flv',
               rtmp]

    pipe = subprocess.Popen(command
                            , shell=False
                            , stdin=subprocess.PIPE
                            )

    while cap.isOpened():
        grabbed, transportation['frame'] = cap.read()
        if grabbed:
            '''
    		对frame进行识别处理
    		'''
            if flag == 0:
                transportation['frame'] = cv2.flip(transportation['frame'], 1)
                # transportation['frame'] = imutils.resize(transportation['frame'], width=500)
                transportation['rgb'] = cv2.cvtColor(transportation['frame'], cv2.COLOR_BGR2RGB)

                if transportation['W'] is None or transportation['H'] is None:
                    (transportation['H'], transportation['W']) = transportation['frame'].shape[:2]

                transportation = checkFence.checkFence(transport=transportation)
                if transportation['intrub']:
                    print("有人入侵")
                    insert_forbid()
                    send_event("在" + str(datetime.datetime.now()) + "有人闯入禁区啦，快去处理一下吧！！！")
                    send_to_front("在" + str(datetime.datetime.now()) + "有人闯入禁区啦，快去处理一下吧！！！")
                # show the output frame
                cv2.imshow("Prohibited Area", transportation['frame'])

                flag = flag - 1
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

                # increment the total number of frames processed thus far and
                # then update the FPS counter
                transportation['totalFrames'] += 1
                transportation['fps'].update()

                pipe.stdin.write(transportation['frame'].tostring())
            else:
                flag = (flag + 1) % 3

    # stop the timer and display FPS information
    transportation['fps'].stop()

    cap.release()
    pipe.terminate()

if __name__ == "__main__":
    camera_fence()