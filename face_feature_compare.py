import face_dll
import face_class
import face_function as fun
import face_feature_extract

'''
本地图片提取的特征值与内存的特征值对比
'''


def face_feature_compare(faceFeature):

    # 结果比对
    faceFeatures = face_feature_extract.loadFaceFeature('images/')

    for item in faceFeatures:

        ret, result = fun.faceFeatureCompare(faceFeature, item['faceFeature'])
        if ret == 0:
            print('name %s similarity %s' % (item['name'], result))


if __name__ == "__main__":
    ret, faceFeature = face_feature_extract.faceFeatureExtract(
        'images/JuJingyi.jpg')

    if ret == 0:
        face_feature_compare(faceFeature)
