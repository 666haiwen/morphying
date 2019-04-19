import os
import numpy as np
import cv2 as cv
import dlib
from ..const import IMG_DIR, MODEL_DIR


class FaceFeatures(object):
    def __init__(self, srcPath, dstPath):
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor( 'shape_predictor_68_face_landmarks.dat')
        self.srcImg = cv.imread(srcPath)
        self.dstImg = cv.imread(dstPath)
        if self.srcImg.shape != self.dstImg.shape:
            shape = self.dstImg.shape
            self.srcImg = cv.resize(self.srcImg, shape, interpolation=cv.INTER_CUBIC)
    
    def __call__(self):
        rects = detector(img_gray, 0)
        for i in range(len(rects)):
            landmarks = np.matrix([[p.x, p.y] for p in predictor(img,rects[i]).parts()])
            for idx, point in enumerate(landmarks):
                # 68点的坐标
                pos = (point[0, 0], point[0, 1])
                print(idx,pos)

                # 利用cv2.circle给每个特征点画一个圈，共68个
                cv2.circle(img, pos, 5, color=(0, 255, 0))
                # 利用cv2.putText输出1-68
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(img, str(idx+1), pos, font, 0.8, (0, 0, 255), 1,cv2.LINE_AA)

cv2.namedWindow("img", 2)
cv2.imshow("img", img)
cv2.waitKey(0)
