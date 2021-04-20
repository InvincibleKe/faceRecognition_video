from ctypes import c_int32, c_char_p, c_void_p, c_float, c_size_t, c_ubyte, c_long, cdll, POINTER, CDLL
from face_class import *
import os
wuyongdll = CDLL(os.path.join(os.path.dirname(__file__), "libarcsoft_face.so"))
dll = CDLL(os.path.join(os.path.dirname(__file__)),'libarcsoft/libarcsoft_face_engine.so')
dllc = CDLL('libc.so.6')
ASF_DETECT_MODE_VIDEO = 0x00000000
ASF_DETECT_MODE_IMAGE = 0xFFFFFFFF
c_ubyte_p = POINTER(c_ubyte)

# 激活
active = dll.ASFActivation
active.restype = c_int32
active.argtypes = (c_char_p, c_char_p)

# 初始化
initEngine = dll.ASFInitEngine
initEngine.restype = c_int32
initEngine.argtypes = (c_long, c_int32, c_int32,
                       c_int32, c_int32, POINTER(c_void_p))

# 人脸识别
detectFaces = dll.ASFDetectFaces
detectFaces.restype = c_int32
detectFaces.argtypes = (c_void_p, c_int32, c_int32,
                        c_int32, POINTER(c_ubyte), POINTER(ASF_MultiFaceInfo))

# 特征提取
faceFeatureExtract = dll.ASFFaceFeatureExtract
faceFeatureExtract.restype = c_int32
faceFeatureExtract.argtypes = (c_void_p, c_int32, c_int32, c_int32, POINTER(
    c_ubyte), POINTER(ASF_SingleFaceInfo), POINTER(ASF_FaceFeature))

# 特征比对
faceFeatureCompare = dll.ASFFaceFeatureCompare
faceFeatureCompare.restype = c_int32
faceFeatureCompare.argtypes = (c_void_p, POINTER(
    ASF_FaceFeature), POINTER(ASF_FaceFeature), POINTER(c_float))
malloc = dllc.malloc
free = dllc.free
memcpy = dllc.memcpy

malloc.restype = c_void_p
malloc.argtypes = (c_size_t, )
free.restype = None
free.argtypes = (c_void_p, )
memcpy.restype = c_void_p
memcpy.argtypes = (c_void_p, c_void_p, c_size_t)

#ASFFaceFeatureExtractEx第二次特征提取
'''
hEngine in 引擎句柄
imgData in 图像数据
faceInfo in 单人脸信息（人脸框、人脸角度）
feature out 提取到的人脸特征信息
'''
faceFeatureExtractEx = dll.ASFFaceFeatureExtractEx
faceFeatureExtractEx.restype = c_int32
faceFeatureExtractEx.argtypes = (c_void_p, POINTER(ASVLOFFSCREEN), POINTER(ASF_SingleFaceInfo), POINTER(ASF_FaceFeature))

#设置RGB/IR活体阈值，若不设置内部默认RGB：0.5 IR：0.7
'''
hEngine in 引擎句柄
threshold in 活体阈值，推荐RGB:0.5 IR:0.7
'''
setLivenessParam = dll.ASFSetLivenessParam
setLivenessParam.restype = c_int32
setLivenessParam.argtypes = (c_void_p, ASF_LivenessThreshold)

#人脸属性检测（年龄/性别/人脸3D角度），最多支持4张人脸信息检测，超过部分返回未知（活体仅支持单张人脸检测，超出返回未知）,接口不支持IR图像检测
'''
hEngine in 引擎句柄

width in 图片宽度，为4的倍数

height in 图片高度，YUYV/I420/NV21/NV12格式为2的倍数；BGR24格式无限制；

format in 支持YUYV/I420/NV21/NV12/BGR24
ASVL_PAF_NV21 2050 8-bit Y 通道，8-bit 2x2 采样 V 与 U 分量交织通道
ASVL_PAF_NV12 2049 8-bit Y 通道，8-bit 2x2 采样 U 与 V 分量交织通道
ASVL_PAF_RGB24_B8G8R8 513 RGB 分量交织，按 B, G, R, B 字节序排布
ASVL_PAF_I420 1537 8-bit Y 通道， 8-bit 2x2 采样 U 通道， 8-bit 2x2 采样 V通道
ASVL_PAF_YUYV 1289 YUV 分量交织， V 与 U 分量 2x1 采样，按 Y0, U0, Y1,V0 字节序排布
ASVL_PAF_GRAY 1793 8-bit IR图像
ASVL_PAF_DEPTH_U16 3074 16-bit IR图像

imgData in 图像数据

detectedFaces in 多人脸信息

combinedMask in 1.检测的属性（ASF_AGE、ASF_GENDER、 ASF_FACE3DANGLE、ASF_LIVENESS），支持多选 2.检测的属性须在引擎初始化接口的combinedMask参数中启用
#define ASF_FACE_DETECT 0x00000001 //人脸检测
#define ASF_FACERECOGNITION 0x00000004 //人脸特征
#define ASF_AGE 0x00000008 //年龄
#define ASF_GENDER 0x00000010 //性别
#define ASF_FACE3DANGLE 0x00000020 //3D角度
#define ASF_LIVENESS 0x00000080 //RGB活体
#define ASF_IR_LIVENESS 0x00000400 //IR活体
多组合 MInt32 processMask = ASF_AGE | ASF_GENDER | ASF_FACE3DANGLE | ASF_LIVENESS;
'''
ASVL_PAF_RGB24_B8G8R8 = 513
process = dll.ASFProcess
process.restype = c_int32
process.argtypes = (c_void_p, c_int32, c_int32, c_int32, POINTER(c_ubyte), ASF_MultiFaceInfo, c_int32)

#人脸信息检测（年龄/性别/人脸3D角度），最多支持4张人脸信息检测，超过部分返回未知（活体仅支持单张人脸检测，超出返回未知）,接口不支持IR图像检测。
'''
hEngine in 引擎句柄
imgData in 图像数据
detectedFaces in 多人脸信息
combinedMask in
    1.检测的属性（ASF_AGE、ASF_GENDER、 ASF_FACE3DANGLE、ASF_LIVENESS），支持多选
    2.检测的属性须在引擎初始化接口的combinedMask参数中启用
'''
processEx = dll.ASFProcessEx
processEx.restype = c_int32
processEx.argtypes = (c_void_p, POINTER(c_ubyte), ASF_MultiFaceInfo, c_int32)

#ASFGetAge 获取年龄信息。
'''
hEngine in 引擎句柄
ageInfo out 检测到的年龄信息数组
'''
getAge = dll.ASFGetAge
getAge.restype = c_int32
getAge.argtypes = (c_void_p, ASF_AgeInfo)

#ASFGetGender 获取性别信息。
'''
hEngine in 引擎句柄
genderInfo out 检测到的性别信息数组
'''
getGender = dll.ASFGetGender
getGender.restype = c_int32
getGender.argtypes = (c_void_p, ASF_GenderInfo)

#ASFGetFace3DAngle 获取3D角度信息。
'''
hEngine in 引擎句柄
p3DAngleInfo out 检测到的3D角度信息数组
'''
getFace3DAngle = dll.ASFGetFace3DAngle
getFace3DAngle.restype = c_int32
getFace3DAngle.argtypes = (c_void_p, ASF_Face3DAngle)

#ASFGetLivenessScore 获取RGB活体信息。
'''
hEngine in 引擎句柄
livenessInfo out 检测到的活体信息
'''
getLivenessScore = dll.ASFGetLivenessScore
getLivenessScore.restype = c_int32
getLivenessScore.argtypes = (c_void_p, ASF_LivenessInfo)

#ASFProcess_IR 该接口仅支持单人脸 IR 活体检测，超出返回未知
'''
hEngine in 引擎句柄
width in 图片宽度，为4的倍数
height in 图片高度
format in 图像颜色格式
imgData in 图像数据
detectedFaces in 多人脸信息
combinedMask in 目前仅支持 ASF_IR_LIVENESS(0x00000400)
'''
process_IR = dll.ASFProcess_IR
process_IR.restype = c_int32
process_IR.argtypes = (c_void_p, c_int32, c_int32, c_int32, POINTER(c_ubyte), ASF_MultiFaceInfo, c_int32)

#ASFProcessEx_IR 该接口仅支持单人脸 IR 活体检测，超出返回未知
'''
hEngine in 引擎句柄
imgData in 图像数据
detectedFaces in 多人脸信息
combinedMask in 目前仅支持 ASF_IR_LIVENESS
'''
processEx_IR = dll.ASFProcessEx_IR
processEx_IR.restype = c_int32
processEx_IR.argtypes = (c_void_p, POINTER(c_ubyte), ASF_MultiFaceInfo, c_int32)

#ASFGetLivenessScore_IR 获取IR活体信息。
'''
hEngine in 引擎句柄
livenessInfo out 检测到的IR活体信息
'''
getLivenessScore_IR = dll.ASFGetLivenessScore_IR
getLivenessScore_IR.restype = c_int32
getLivenessScore_IR.argtypes = (c_void_p, POINTER(c_ubyte), ASF_LivenessInfo)

#ASFGetVersion 获取SDK版本信息。
'''
'''
getVersion = dll.ASFGetVersion
getVersion.restype = ASF_VERSION

#ASFUninitEngine 销毁SDK引擎。
'''
hEngine in 引擎句柄
'''
uninitEngine = dll.ASFUninitEngine
uninitEngine.restype = c_int32
uninitEngine.argtypes = (c_void_p,)