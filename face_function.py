import face_dll
import face_class
from ctypes import *
import cv2
from io import BytesIO

# from Main import *
Handle = c_void_p()
c_ubyte_p = POINTER(c_ubyte)

# 激活函数


def active(appkey, sdkey):
    ret = face_dll.active(appkey, sdkey)
    return ret

# 初始化函数


def init(model):
    '''
        1 视频(0x00000000)或图片(0xFFFFFFFF)模式,
        2 角度(),
        3 识别的最小人脸比例 = 图片长边 / 人脸框长边的比值 默认推荐值：VIDEO模式推荐16；IMAGE模式推荐32
        4 最大需要检测的人脸个数，取值范围[1,50],
        5 需要启用的功能组合，可多选ASF_FACE_DETECT 0x00000001 //人脸检测 SF_FACERECOGNITION 0x00000004 //人脸特征 ASF_AGE 0x00000008 //年龄 ASF_GENDER 0x00000010 //性别
        ASF_FACE3DANGLE 0x00000020 //3D角度 ASF_LIVENESS 0x00000080 //RGB活体 ASF_IR_LIVENESS 0x00000400 //IR活体 这些属性均是以常量值进行定义，可通过 | 位运算符进行组合使用。
        例如 MInt32 combinedMask = ASF_FACE_DETECT | ASF_FACERECOGNITION | ASF_LIVENESS;
        6 返回激活句柄
    '''
    ret = face_dll.initEngine(model, 0x1, 16, 10, 5, byref(Handle))
    return ret, Handle

# cv2记载图片并处理


def LoadImg(imageData):

    img = cv2.imread(imageData.filepath)
    sp = img.shape

    img = cv2.resize(img, (sp[1]//4*4, sp[0]//4*4))
    sp = img.shape

    imageData.image = img
    imageData.width = sp[1]
    imageData.height = sp[0]

    return imageData


'''
处理图片改变大小
'''


def deal_image_data(imageData):

    shape = imageData.image.shape

    image = cv2.resize(imageData.image, (shape[1]//4*4, shape[0]//4*4))
    shape = image.shape

    imageData.image = image
    imageData.width = shape[1]
    imageData.height = shape[0]

    return imageData


def detectFaces(imageData):
    faces = face_class.ASF_MultiFaceInfo()
    imgby = bytes(imageData.image)
    imgcuby = cast(imgby, c_ubyte_p)
    ret = face_dll.detectFaces(
        Handle, imageData.width, imageData.height, 0x201, imgcuby, byref(faces))
    return ret, faces

# 显示人脸识别图片


def showimg(im, faces):
    for i in range(0, faces.faceNum):
        ra = faces.faceRect[i]
        cv2.rectangle(im.image, (ra.left, ra.top),
                      (ra.right, ra.bottom), (255, 0, 0,), 2)

    cv2.imshow('faces', im.image)
    cv2.waitKey(0)

# 显示人脸识别图片


def showimg2(imageData, faces, faceFeatures, faceInfos):

    for i in range(0, faces.faceNum):
        # 画出人脸框
        ra = faces.faceRect[i]
        cv2.rectangle(imageData.image, (ra.left, ra.top),
                      (ra.right, ra.bottom), (255, 0, 0,), 2)

        peopleName = 'unknown'
        res = 0.5

        # 提取单人1特征
        ft = getsingleface(faces, i)
        ret, faceFeature = faceFeatureExtract(imageData, ft)

        if ret == 0:
            for item in faceFeatures:
                ret, result = faceFeatureCompare(
                    faceFeature, item['faceFeature'])
                if ret == 0:
                    if result > res:
                        res = result
                        peopleName = faceInfos[item['id']]['name']

        cv2.putText(imageData.image, peopleName, (ra.left, ra.top - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0,), 1, cv2.LINE_AA)

    cv2.imshow('faces', imageData.image)


def deal_frame(imageData, faces, faceFeatures, faceInfos):

    for i in range(0, faces.faceNum):
        # 画出人脸框
        ra = faces.faceRect[i]
        cv2.rectangle(imageData.image, (ra.left, ra.top),
                      (ra.right, ra.bottom), (255, 0, 0,), 2)

        peopleName = 'unknown'
        res = 0.5

        # 提取单人1特征
        ft = getsingleface(faces, i)
        ret, faceFeature = faceFeatureExtract(imageData, ft)

        if ret == 0:
            for item in faceFeatures:
                ret, result = faceFeatureCompare(
                    faceFeature, item['faceFeature'])
                if ret == 0:
                    if result > res:
                        res = result
                        peopleName = faceInfos[item['id']]['name']

        cv2.putText(imageData.image, peopleName, (ra.left, ra.top - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0,), 1, cv2.LINE_AA)

    return imageData.image
# 提取人脸特征


def faceFeatureExtract(im, ft):
    detectedFaces = face_class.ASF_FaceFeature()
    img = im.image
    imgby = bytes(im.image)
    imgcuby = cast(imgby, c_ubyte_p)

    ret = face_dll.faceFeatureExtract(
        Handle, im.width, im.height, 0x201, imgcuby, ft, byref(detectedFaces))
    if ret == 0:
        retz = face_class.ASF_FaceFeature()
        retz.featureSize = detectedFaces.featureSize
        # 必须操作内存来保留特征值,因为c++会在过程结束后自动释放内存
        retz.feature = face_dll.malloc(detectedFaces.featureSize)
        face_dll.memcpy(retz.feature, detectedFaces.feature,
                        detectedFaces.featureSize)
        return ret, retz
    else:
        return ret, None

# 特征值比对,返回比对结果


def faceFeatureCompare(faceFeature1, FaceFeature2):
    result = c_float()
    ret = face_dll.faceFeatureCompare(
        Handle, faceFeature1, FaceFeature2, byref(result))
    return ret, result.value

# 单人特征写入文件


def writeFTFile(feature, filepath):
    f = BytesIO(string_at(feature.feature, feature.featureSize))
    a = open(filepath, 'wb')
    a.write(f.getvalue())
    a.close()

# 从多人中提取单人数据


def getsingleface(singleface, index):

    ft = face_class.ASF_SingleFaceInfo()
    ra = singleface.faceRect[index]
    ft.faceRect.left = ra.left
    ft.faceRect.right = ra.right
    ft.faceRect.top = ra.top
    ft.faceRect.bottom = ra.bottom
    ft.faceOrient = singleface.faceOrient[index]

    return ft

# 从文件获取特征值


def ftfromfile(filepath):
    fas = face_class.ASF_FaceFeature()
    f = open(filepath, 'rb')
    b = f.read()
    f.close()
    fas.featureSize = b.__len__()
    fas.feature = face_dll.malloc(fas.featureSize)
    face_dll.memcpy(fas.feature, b, fas.featureSize)
    return fas
