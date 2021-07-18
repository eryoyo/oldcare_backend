import cv2
import subprocess
import dlib
import numpy
# from skimage import io
import cv2
import time
from PIL import Image, ImageDraw, ImageFont
import math
import os
from model.functions.dlibPoint import FaceRecord


def camera_collect(rtsp):
    # rtsp = "rtmp://192.144.218.105/live/1_1"
    # rtmp = 'rtmp://192.144.218.105/live/1_1_back'
    rtmp = rtsp + "_back"

    # 用户id
    start = rtsp.rindex('/')
    userid = rtsp[start + 1:]
    path = os.getcwd()
    print(path)
    path = os.getcwd() + "/image/" + userid
    if not os.path.exists(path):
        os.mkdir(path)

    # 操作顺序及所需照片数
    operation_process = [
        ["mouth_open", 10],
        # ["eye_close",10],
        ["face_up", 10],
        ["face_down", 10],
        ["face_right", 10],
        ["face_left", 10],
    ]

    faceRecord = FaceRecord()

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

    for (type, count) in operation_process:
        i = 1
        while (i <= count):
            ret, img = cap.read()
            img, check = faceRecord.face_image_process(img, path, photo_name=type + "_" + str(i), display_type="rect",
                                                       detect_pos=type)
            if check:
                i = i + 1
            cv2.imshow('img', img)
            pipe.stdin.write(img.tostring())
            k = cv2.waitKey(100) & 0xff
            if k == 27:
                break

    cap.release()
    pipe.terminate()


if __name__ == "__main__":
    camera_collect()
