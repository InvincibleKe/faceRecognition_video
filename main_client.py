import face_dll
import face_class
from ctypes import *
import cv2
import face_function as fun
import face_feature_extract

Appkey = b''
SDKey = b''

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


def start(faceFeatures):
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    while True:
        # get a frame
        ret, frame = cap.read()
        if ret:
            # 加载图片
            imageData = face_class.ImageData(frame, frame_width, frame_height)
            ret, faces = fun.detectFaces(fun.deal_image_data(imageData))
            if ret == 0:
                fun.showimg2(imageData, faces, faceFeatures, faceInfos)
            else:
                pass

        # show a frame
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # active()
    # 加载人脸资源
    faceFeatures = face_feature_extract.load_face_feature(faceInfos)
    init()
    start(faceFeatures)
