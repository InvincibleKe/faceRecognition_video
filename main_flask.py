
import face_function as fun
import face_feature_extract
import video_camera
import time
from flask import Flask, abort, request, jsonify, Response

app = Flask(__name__)

Appkey = b'7TYaMJwpuLeHMWGvEiruNkMVsKBQ6avMf9p9fAVLUHCi'
SDKey = b'2rdWNdJaVEaaJTDZ1C4hAJbe4d2d4RQwpdn6rFwmtMvH'

'''
存放人脸库的信息,key为对应的图片名即为1.jpg或者2.jpg
'''
faceInfos = {'1':{'name':'Ju Jingyi','gender':'girl','age':'25','image':'images/1.jpg'},'2':{'name':'Ju Jingyi','gender':'girl','age':'25','image':'images/2.jpg'}}


'''
激活sdk,激活一次即可
'''


def active():
    ret = fun.active(Appkey, SDKey)
    if ret == 0 or ret == 90114:
        print('激活成功:', ret)
    else:
        print('激活失败:', ret)
        pass


def init():
    # 初始化 1 视频(0x00000000)或图片(0xFFFFFFFF)模式,
    ret = fun.init(0x00000000)
    if ret[0] == 0:
        print('初始化成功:', ret, '句柄', fun.Handle)
    else:
        print('初始化失败:', ret)

def gen():
    
    videoCamera = video_camera.VideoCamera(faceFeatures, faceInfos)

    while True:
        ret, frame = videoCamera.get_frame()
        if ret:
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n\r\n')
            time.sleep(0.1)
'''
返回图片流
'''
@app.route('/faceRecognition_video')
def video_feed():
    return Response(gen(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    active()
    # 加载人脸资源
    faceFeatures = face_feature_extract.load_face_feature(faceInfos)
    init()
    app.run(host="0.0.0.0", port=8080, debug=True, threaded=True, processes=True)
