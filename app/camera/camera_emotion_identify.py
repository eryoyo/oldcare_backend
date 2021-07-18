import cv2
import subprocess
import time

from app.wechat.api import send_event
from model.functions.FullEmotion import EmotionDetect
from app.event.api import insert_emotion, insert_interrupt, send_to_front
import datetime


def camera_emotion_identify():
    rtsp = "rtmp://192.144.218.105/live/emotion_identify_in"
    rtmp = 'rtmp://192.144.218.105/live/emotion_identify'

    # starting video streaming
    transportation = {
        'frame': None, 'stranger': False, 'stranger_time': 0, 'result': [], 'result_timer': {}
    }
    emotionDetect = EmotionDetect()
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
        success, frame = cap.read()
        if success:
            '''
    		对frame进行识别处理
    		'''
            if flag == 0:
                transportation['frame'] = frame
                transportation = emotionDetect.checkEmotion(transportation)
                cv2.imshow('window_frame', transportation['frame'])
                if transportation['stranger']:
                    print("陌生人闯入房间")
                    insert_interrupt()
                    send_event("在" + str(datetime.datetime.now()) + "有人闯入房间啦，快去处理一下吧！！！")
                    send_to_front("在" + str(datetime.datetime.now()) + "有人闯入房间啦，快去处理一下吧！！！")
                for result in transportation['result']:
                    print(result[0] + result[1])
                    insert_emotion(result[1], int(result[0]))
                    send_event("在" + str(datetime.datetime.now()) + "老人" + result[0] + "正在" + result[1] + "！！！")
                    send_to_front("在" + str(datetime.datetime.now()) + "老人" + result[0] + "正在" + result[1] + "！！！")
                flag = flag - 1
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                pipe.stdin.write(transportation['frame'].tostring())
            else:
                flag = (flag + 1) % 3

    cap.release()
    pipe.terminate()

if __name__ == "__main__":
    camera_emotion_identify()