import cv2
import face_function as fun
import face_feature_extract
import face_class

'''
摄像头类
'''


class VideoCamera(object):
    def __init__(self, faceFeatures, faceInfos):
        # 通过opencv获取实时视频流
        self.videoCapture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.frame_width = int(self.videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(
            self.videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.faceFeatures = faceFeatures
        self.faceInfos = faceInfos

    def __del__(self):
        self.videoCapture.release()

    '''
    将视频帧转换为字节流返回
    '''

    def get_frame(self):
        ret, frame = self.videoCapture.read()
        if ret:
            # 加载图片
            imageData = face_class.ImageData(
                frame, self.frame_width, self.frame_height)
            ret, faces = fun.detectFaces(fun.deal_image_data(imageData))
            if ret == 0:
                frame = fun.deal_frame(
                    imageData, faces, self.faceFeatures, self.faceInfos)
            img_fps = 80
            img_param = [int(cv2.IMWRITE_JPEG_QUALITY), img_fps]
            # 转化
            ret, frame = cv2.imencode('.jpg', frame, img_param)
        return ret, frame
