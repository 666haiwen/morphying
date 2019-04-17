import numpy as np
import cv2 as cv
import os
import  imageio
from const import *


class Morphing(object):
    def __init__(self, srcPath, dstPath):
        self.srcImg = cv.imread(srcPath)
        self.dstImg = cv.imread(dstPath)
        if self.srcImg.shape != self.dstImg.shape:
            self.srcImg = cv.resize(self.srcImg, SIZE, interpolation=cv.INTER_CUBIC)
            self.dstImg = cv.resize(self.dstImg, SIZE, interpolation=cv.INTER_CUBIC)
        # self.newDstImg = np.ones(self.dstImg.shape) * 255
        self.mask = np.ones(self.dstImg.shape[:2])
        self.cnt = 0
        self.numberSave = 0
        self.newDstImg = self.dstImg.copy()
        self.size = self.srcImg.shape
        self.imgList = []
        self.crossImgList = []

    def distance(self, p, q):
        """
            calculate the distance between p and q
            @params:
                p: 2-darray
                q: 2-darray
            @returns:
                dis: float
        """
        return np.sqrt(np.dot((p - q), (p - q)))

    def setPixel(self, X, X_):
        """
            merge the srcImg and dstImg by feature-lines
        """
        x, y = X[0], X[1]
        x_ = max(min(int(X_[0]), self.size[1] - 1),0) 
        y_ = max(min(int(X_[1]), self.size[0] - 1),0)
        self.newDstImg[y][x] = self.srcImg[y_][x_]
        # self.cnt += 1
        # if self.cnt % 50 == 0:
        #     cv.imwrite(RESULT_DIR + '/cnt_{}.png'.format(self.numberSave), self.newDstImg)
        #     self.numberSave += 1
        self.mask[y][x] = 255

    def cross_dissolve(self, alpha=0.05):
        """
            morphing by cross_dissolve
            @param:
                alpha: the step to close the dst img, default = 0.05
            @return:
                imgList: the list of transfer imgs
        """
        t = 0
        imgList = []
        while t < 1:
            tmpImg = np.uint8(self.newDstImg * (1 - t) + self.dstImg * t)
            imgList.append(tmpImg.copy())
            t += alpha
        imgList.append(self.dstImg)
        return imgList

    def single_line(self, src, dst, X):
        """
            calculate the new postion of X' by single line-pair
            @params:
                src: {'P', 'Q', 'length'}, P, Q and length
                dst: {'P', 'Q', 'length'}, P', Q' and length
                X: ndarray(2,), orignal postion of X
            @return:
                X': ndarray(2,) new postion
                weight: float
        """
        diff_XP = X - src['P']
        diff_QP = src['Q'] - src['P']
        per_QP = diff_QP[::-1] * np.array([1, -1])
        u = np.dot(diff_XP, diff_QP) / np.dot(diff_QP, diff_QP)
        v = np.dot(diff_XP, per_QP) / np.sqrt(np.dot(diff_QP, diff_QP))

        diff_QP_dst = dst['Q'] - dst['P']
        per_QP_dst = diff_QP_dst[::-1] * np.array([1, -1])
        X_ = dst['P'] + u * (dst['Q'] - dst['P']) + v * per_QP_dst / np.sqrt(np.dot(diff_QP_dst, diff_QP_dst))
        if u < 0:
            dist = self.distance(X, src['P'])
        elif u > 1:
            dist = self.distance(X, src['Q'])
        else:
            dist = abs(v)
        weight = (src['length'] ** P / (A + dist)) ** B
        return X_, weight

    def multi_line(self, lines_src, lines_dst):
        """
            warping by muli-features-lines.
            @params:
                lines_src: the list of src img's feature lines
                lines_dst: the list of dst img's feature lines
        """
        number = min(len(lines_src), len(lines_dst))
        if number == 0:
            self.newDstImg = self.srcImg
            return
        size = self.srcImg.shape
        for x in range(size[1]):
            for y in range(size[0]):
                newX = np.zeros(2)
                weightSum = 0
                for i in range(number):
                    x_, weight = self.single_line(lines_dst[i], lines_src[i], (x, y))
                    newX += x_ * weight
                    weightSum += weight
                newX /= weightSum
                self.setPixel((x,y), newX)
        # self.newDstImg = (self.newDstImg + self.dstImg) / 2
        tmp = (self.dstImg + self.srcImg) / 2
        cv.imwrite(RESULT_DIR + '/orignal.png', tmp)
        cv.imwrite(RESULT_DIR + '/merge.png', self.newDstImg)
        cv.imwrite(RESULT_DIR + '/mask.png', self.mask)

    def save_Gifs(self, name):
        """
            save the result by morphying.
            Such as gif and transfer processing.
        """
        imgTransfer = np.zeros((self.size[0], self.size[1] * 6, self.size[2]))
        imgTransfer[:,:self.size[1]] = self.newDstImg
        imgTransfer[:,self.size[1] * 5:] = self.dstImg
        index = 0
        path = RESULT_DIR + '/{}.gif'.format(name)
        with imageio.get_writer(path, mode='i', duration=0.1) as writer:
            length = len(self.imgList)
            middle_res = [int(v * length) for v in [0.2, 0.4, 0.6, 0.8]]
            for i, img in enumerate(self.imgList):
                if i in middle_res:
                    index += 1
                    imgTransfer[:, self.size[1] * index : self.size[1] * (index + 1)] = img
                writer.append_data(img[:,:,::-1])
        path = RESULT_DIR + '/{}_middle_transfer.png'.format(name)
        cv.imwrite(path, imgTransfer)

    def __call__(self, lines_src, lines_dst, name, alpha=0.05):
        self.multi_line(lines_src, lines_dst)
        # feature-based Image Metamorphosis
        self.imgList = self.cross_dissolve(alpha)
        self.save_Gifs(name)
        # Just cross_dissolve
        self.newDstImg = self.srcImg
        self.imgList = self.cross_dissolve(alpha)
        self.save_Gifs(name + '_cross_dissovle')
