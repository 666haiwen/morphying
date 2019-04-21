import numpy as np
import cv2 as cv
from utils import cross_dissolve
from const import P, A, B


class Morphing(object):
    """
        Morphing by muli-features-lines by Beier and Neely.
        @papers: http://www.indiana.edu/~pcl/busey/morph.pdf
    """
    def __init__(self, srcImg, dstImg):
        self.srcImg = srcImg
        self.dstImg = dstImg
        if self.srcImg.shape != self.dstImg.shape:
            self.srcImg = cv.resize(self.srcImg, self.dstImg.shape, interpolation=cv.INTER_CUBIC)
        self.newDstImg = self.dstImg.copy()
        self.size = self.srcImg.shape

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
        x_ = max(min(int(X_[0]), self.size[1] - 1), 0)
        y_ = max(min(int(X_[1]), self.size[0] - 1), 0)
        self.newDstImg[y][x] = self.srcImg[y_][x_]

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

        for x in range(self.size[1]):
            for y in range(self.size[0]):
                newX = np.zeros(2)
                weightSum = 0
                for i in range(number):
                    x_, weight = self.single_line(lines_dst[i], lines_src[i], (x, y))
                    newX += x_ * weight
                    weightSum += weight
                newX /= weightSum
                self.setPixel((x,y), newX)

    def __call__(self, lines_src, lines_dst, interval):
        self.multi_line(lines_src, lines_dst)
        return cross_dissolve(self.newDstImg, self.dstImg, interval)
