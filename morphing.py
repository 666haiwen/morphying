import numpy as np
import cv2 as cv
import os
import  imageio
from const import *
from matplotlib import pyplot as plt
from matplotlib import image as mpimg



class Morphing(object):
    def __init__(self, srcPath, dstPath):
        self.srcImg = self.readImage(srcPath)
        self.dstImg = self.readImage(dstPath)
        self.imgList = []

    def readImage(self, path):
        return mpimg.imread(path)[:,:,:3]


    def cross_dissolve(self, alpha=0.01):
        t = 0
        while t < 1:
            tmpImg = np.uint8(self.srcImg * (1 - t) + self.dstImg * t)
            self.imgList.append(tmpImg.copy())
            t += alpha
        imgList.append(self.dstImg)
        return self.imgList


    def single_line(self, P_src, Q_src, P_dst, Q_dst, X):
        """
            calculate the new postion of X' by single line-pair
            @params:
                P_src: ndarray(2,), P
                Q_src: ndarray(2,), Q
                P_dst: ndarray(2,), P'
                Q_dst: ndarray(2,), Q'
                X: ndarray(2,), orignal postion of X
            @return:
                X': ndarray(2,) new postion
        """
        diff_XP = X - P_src
        diff_QP = Q_src - P_src
        per_QP = diff_QP[::-1] * np.array([1, -1])
        u = np.dot(diff_XP, diff_QP) / np.dot(diff_QP, diff_QP)
        v = np.dot(diff_XP, per_QP) / np.sqrt(np.dot(diff_QP, diff_QP))

        diff_QP_dst = Q_dst - P_dst
        per_QP_dst = diff_QP_dst[::-1] * np.array([1, -1])
        return P_dst + u*(Q_dst - P_dst) + v * per_QP_dst / np.sqrt(np.dot(diff_QP_dst, diff_QP_dst))


    def multi_line(self, line_src, line_dst):
        pass


    def save_Gifs(self, path):
        with imageio.get_writer(path, mode='i', duration=0.1) as writer:
            for img in self.imgList:
                writer.append_data(img)

