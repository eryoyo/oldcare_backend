import datetime

import cv2
import subprocess
import time

from app.event.api import send_to_front, insert_falldown
# from app.utils.tool import send_to_all
from app.wechat.api import send_event
from model.functions.falldetectionbone import FallDetectionBone
from model.Model.Detection.Utils import ResizePadding


def camera_fall():
    rtsp = "rtmp://192.144.218.105/live/fall_in"
    rtmp = 'rtmp://192.144.218.105/live/fall'

    # starting video streaming
    transportation = {'status': 0, 'frame': None, 'fall_flag': 0,
                      'fall': False, 'last_fall': 0}
    flag = 0

    # 读取视频并获取属性
    cap = cv2.VideoCapture(rtsp)
    cap.set(0, 640)  # set Width (the first parameter is property_id)
    cap.set(1, 480)  # set Height
    time.sleep(2)
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    sizeStr = str(size[0]) + 'x' + str(size[1])
    resize_fn = ResizePadding(384, 384)

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

    fallDetectionBone = FallDetectionBone(device='cpu')
    while cap.isOpened():
        transportation['status'] = 0
        (grabbed, transportation['frame']) = cap.read()
        img = transportation['frame']
        if grabbed:
            '''
    		对frame进行识别处理
    		'''
            if flag == 0:
                transportation['frame'] = cv2.flip(transportation['frame'], 1)

                transportation['frame'] = resize_fn(transportation['frame'])
                transportation['frame'] = cv2.cvtColor(transportation['frame'], cv2.COLOR_BGR2RGB)

                transportation = fallDetectionBone.run(transportation)

                if transportation['fall']:
                    print('有人摔倒了')
                    insert_falldown()
                    send_event("在" + str(datetime.datetime.now()) + "有人在走廊摔倒啦，快去处理一下吧！！！")
                    send_to_front("在" + str(datetime.datetime.now()) + "有人在走廊摔倒啦，快去处理一下吧！！！")
                    # # 生成摔倒截图
                    # cv2.imwrite(os.path.join(output_fall_path, 'snapshot_%s.jpg' % (time.strftime('%Y%m%d_%H%M%S'))),
                    #             transportation['frame'])

                cv2.imshow('frame', transportation['frame'])
                flag = flag - 1
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                pipe.stdin.write(img.tostring())
            else:
                flag = (flag + 1) % 7

    cap.release()
    pipe.terminate()

if __name__ == "__main__":
    camera_fall()