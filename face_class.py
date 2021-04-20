from ctypes import c_int32, c_char_p, Structure, POINTER, c_void_p, c_float, c_int8, c_uint32

# 人脸框
'''
MRECT* faceRect 人脸框数组
MInt32* faceOrient 人脸角度数组
MInt32 faceNum 检测到的人脸数
MInt32* faceID 一张人脸从进入画面直到离开画面，faceID不变。
在VIDEO模式下有效，IMAGE模式下为空

'''

class MRECT(Structure):
    _fields_ = [(u'left', c_int32), (u'top', c_int32),
                (u'right', c_int32), (u'bottom', c_int32)]

# 版本信息     版本号,构建日期,版权说明
'''
MPChar Version 版本号
MPChar BuildDate 构建日期
MPChar CopyRight 版权说明
'''

class ASF_VERSION(Structure):
    _fields_ = [('Version', c_char_p), ('BuildDate',
                                        c_char_p), ('CopyRight', c_char_p)]

# 单人人脸信息  人脸狂,人脸角度
'''
MRECT faceRect 人脸框
MInt32 faceOrient 人脸角度
'''

class ASF_SingleFaceInfo(Structure):
    _fields_ = [('faceRect', MRECT), ('faceOrient', c_int32)]

# 多人人脸信息 人脸框数组,人脸角度数组,人脸数
'''
MRECT* faceRect 人脸框数组
MInt32* faceOrient 人脸角度数组
MInt32 faceNum 检测到的人脸数
MInt32* faceID 一张人脸从进入画面直到离开画面，faceID不变。在VIDEO模式下有效，IMAGE模式下为空
'''

class ASF_MultiFaceInfo(Structure):
    _fields_ = [(u'faceRect', POINTER(MRECT)), (u'faceOrient',
                                                POINTER(c_int32)), (u'faceNum', c_int32)]

# 人脸特征 人脸特征,人脸特征长度
'''
MByte* feature 人脸特征
MInt32 featureSize 人脸特征长度
'''

class ASF_FaceFeature(Structure):
    _fields_ = [('feature', c_void_p), ('featureSize', c_int32)]

# 自定义图片类


class ImageData:
    def __init__(self, image, width, height):
        self.image = image
        self.width = width
        self.height = height

# 自定义图片类


class ImageLoadData:
    def __init__(self, filepath):
        self.filepath = filepath
        self.image = None
        self.width = 0
        self.height = 0

#年龄信息
'''
MInt32* ageArray 0:未知; >0:年龄
MInt32 num 检测的人脸数
'''
class ASF_AgeInfo(Structure):
    _fields_ = [('ageArray', POINTER(c_int32)), ('num', c_int32)]

#性别信息
'''
MInt32* genderArray 0:男性; 1:女性; -1:未知
MInt32 num 检测的人脸数
'''
class ASF_GenderInfo(Structure):
    _fields_ = [('genderArray', POINTER(c_int32)), ('num', c_int32)]

#3D角度信息
'''
MFloat* roll 横滚角
MFloat* yaw 偏航角
MFloat* pitch 俯仰角
MInt32* status 0:正常; 非0:异常
MInt32 num 检测的人脸个数
'''
class ASF_Face3DAngle(Structure):
    _fields_ = [('roll', POINTER(c_float)), ('yaw', POINTER(c_float)), ('pitch', POINTER(c_float)), ('status', POINTER(c_int32)), ('num', c_int32)]

#活体置信度
'''
MFloat thresholdmodel_BGR BGR活体检测阈值设置，默认值0.5
MFloat thresholdmodel_IR IR活体检测阈值设置，默认值0.7
'''
class ASF_LivenessThreshold(Structure):
    _fields_ = [('thresholdmodel_BGR', c_float), ('thresholdmodel_IR', c_float)]

#活体信息
'''
MInt32* isLive 0:非真人； 1:真人；-1：不确定； -2:传入人脸数 > 1；-3: 人脸过小；-4: 角度过大；-5: 人脸超出边界
MInt32 num 检测的人脸个数
'''
class ASF_LivenessInfo(Structure):
    _fields_ = [('isLive', POINTER(c_int32)), ('num', c_int32)]

#图像数据信息，该结构体在 asvloffscreen. 基础的头文件中
'''
MUInt32 u32PixelArrayFormat 颜色格式
MInt32 i32Width 图像宽度
MInt32 i32Height 图像高度
MUInt8** ppu8Plane 图像数据
MInt32* pi32Pitch 图像步长
'''
class ASVLOFFSCREEN(Structure):
    _fields_ = [('u32PixelArrayFormat', c_uint32), ('i32Width', c_int32), ('i32Height', c_int32), ('ppu8Plane', POINTER(POINTER(c_int32))), ('pi32Pitch', POINTER(c_int32))]
