import face_dll
import face_class
import cv2
import face_function as fun
import os
from ctypes import string_at

'''
存放人脸特征值的集合
'''
faceFeatures = []


'''
初始化sdk设置为图片模式以加载更为精确的特征值集合
'''


def init():
    # 初始化
    ret = fun.init(0xFFFFFFFF)
    if ret[0] == 0:
        print('初始化成功:', ret, '句柄', fun.Handle)
    else:
        print('初始化失败:', ret)


'''
提取图片文件里面的人脸特征值
'''


def face_feature_extract(filepath):

    imageData = face_class.ImageLoadData(filepath)
    imageData = fun.LoadImg(imageData)
    ret, faces = fun.detectFaces(imageData)

    if ret == 0:
        # 提取单人1特征
        ft = fun.getsingleface(faces, 0)
        ret, faceFeature = fun.faceFeatureExtract(imageData, ft)

    return ret, faceFeature


'''
读取人脸资源库所有的图片
'''


def read_images(filePath):
    for i, j, files in os.walk(filePath):
        return files


def load_face_feature(faceInfos):
    init()

    for info in faceInfos:
        imagePath = faceInfos[info]['image']
        if imagePath.find('.jpg'):
            ret, faceFeature = face_feature_extract(imagePath)
            if ret == 0:
                print("add faceFeature", info)
                faceFeatures.append({'id': info, 'faceFeature': faceFeature})

    return faceFeatures


if __name__ == "__main__":
    faceInfos = {'1':{'name':'Ju Jingyi','gender':'girl','age':'25','image':'images/1.jpg'},'2':{'name':'Ju Jingyi','gender':'girl','age':'25','image':'images/2.jpg'}}
    load_face_feature(faceInfos)
