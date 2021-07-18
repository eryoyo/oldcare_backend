import cv2
import subprocess
import time

from app.event.api import insert_interact, send_to_front
# from app.utils.tool import send_to_all
from app.wechat.api import send_event
from model.functions.checkvolunteeractivity import CheckVolunteerActivity


def camera_interact():
    rtsp = "rtmp://192.144.218.105/live/interact_in"
    rtmp = 'rtmp://192.144.218.105/live/interact'

    # starting video streaming
    transportation = {'frame': None, 'status': 0, 'inter_id': 0, 'camera_turned': 0, 'camera_adjust': 'middle',
                      'camera_angle': 0, 'interact_time': {}, 'interact_list': []}
    flag = 0

    # 全局常量
    VIDEO_WIDTH = 640
    VIDEO_HEIGHT = 480

    # 读取视频并获取属性
    cap = cv2.VideoCapture(rtsp)
    cap.set(0, VIDEO_WIDTH)  # set Width (the first parameter is property_id)
    cap.set(1, VIDEO_HEIGHT)  # set Height
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

    checkVolunteerActivity = CheckVolunteerActivity(VIDEO_WIDTH, VIDEO_HEIGHT)
    while cap.isOpened():
        (grabbed, transportation['frame']) = cap.read()
        if grabbed:
            '''
    		对frame进行识别处理
    		'''
            if flag == 0:
                transportation['frame'] = cv2.flip(transportation['frame'], 1)
                transportation = checkVolunteerActivity.run(transportation)
                if len(transportation['interact_list']) != 0:
                    for (old, worker) in transportation['interact_list']:
                        print("%s,%s" % (old, worker))
                        insert_interact(int(old), int(worker))
                        send_event("老人" + old + "和义工" + worker + "进行了亲切友好的互动，这个养老院真不错！！！")
                        send_to_front("老人" + old + "和义工" + worker + "进行了亲切友好的互动，这个养老院真不错！！！")
                # show our detected faces along with smiling/not smiling labels
                cv2.imshow("Checking Volunteer's Activities", transportation['frame'])
                flag = flag - 1
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                pipe.stdin.write(transportation['frame'].tostring())
            else:
                flag = (flag + 1) % 3

    cap.release()
    pipe.terminate()


if __name__ == "__main__":
    camera_interact()
