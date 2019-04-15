import numpy as np
import cv2 as cv

class ImageWindow(object):
    def __init__(self, src, dst, name):
        shape = src.shape
        self.img = np.zeros((shape[0] * 2 + 50,) + shape[1:], np.uint8)
        self.img[:shape[0], :, :] = src
        self.img[shape[0] + 50:, :, :] = dst
        self.points = []
        self.length = []
        self.point_number = 0
        self.color = (0, 152, 255)
        self.name = name

    def draw_line(self, event, x, y, flags, param):
        if event == cv.EVENT_LBUTTONDOWN:
            self.point_number += 1
            self.points.append(np.array([x, y]))
            cv.circle(self.img, (x,y), 3, self.color, -1)
            if self.point_number % 2 == 0:
                first_point = self.points[-2]
                src = (first_point[0], first_point[1])
                dst = (x, y)
                cv.line(self.img, src, dst, self.color, 3)

    def interface_window(self):
        cv.namedWindow(self.name)
        cv.setMouseCallback(self.name, self.draw_line)
        while(1):
            cv.imshow(self.name, self.img)
            k = cv.waitKey(1) & 0xFF
            if k == 27:
                break
        cv.destroyAllWindows()
