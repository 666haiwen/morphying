import numpy as np
import cv2 as cv
from morphing import Morphing


class ImageWindow(object):
    def __init__(self, src, dst, name):
        # height * width * 3
        self.shape = shape = src.shape
        self.img = np.zeros((shape[0] * 2 + 50,) + shape[1:], np.uint8)
        self.img[:shape[0], :, :] = src
        self.img[shape[0] + 50:, :, :] = dst
        self.pre_point = 0
        self.top_points = []
        self.down_points = []
        self.length = []
        self.point_number = 0
        self.color = (0, 152, 255)
        self.name = name


    def mouse_event(self, event, x, y, flag, param):
        """
            Mouse event func applied to cv windows.
        """
        def draw_line(points):
            src = (points[0][0], points[0][1])
            dst = (points[1][0], points[1][1])
            cv.line(self.img, src, dst, self.color, 3)

        if event == cv.EVENT_LBUTTONDOWN:
            if y < self.shape[0] and self.pre_point != 1:
                self.top_points.append(np.array([x, y]))
                cv.circle(self.img, (x,y), 3, self.color, -1)
                pre_point = -1
                if len(self.top_points) % 2 == 0:
                    pre_point = 0
                    draw_line(self.top_points[-2:])
            if y > self.shape[0] + 50 and self.pre_point != -1:
                self.down_points.append(np.array([x, y]))
                cv.circle(self.img, (x,y), 3, self.color, -1)
                pre_point = 1
                if len(self.down_points) % 2 == 0:
                    pre_point = 0
                    draw_line(self.down_points[-2:])


    def interface_window(self):
        cv.namedWindow(self.name)
        cv.setMouseCallback(self.name, self.mouse_event)
        while(1):
            cv.imshow(self.name, self.img)
            k = cv.waitKey(1) & 0xFF
            # esc or enter
            if k == 27 or k == 13:
                break
        cv.destroyAllWindows()
        def distance(x, y):
            return np.sqrt(np.dot((x - y), (x - y)))

        def set_line(points, bias=[0,0]):
            lines = []
            number = len(points)
            for i in range(0, number, 2):
                lines.append({
                    'P': points[i] + bias,
                    'Q': points[i + 1] + bias,
                    'length': distance(points[i], points[i + 1])
                })
            return lines
        return set_line(self.top_points), set_line(self.down_points, [0, -self.shape[0] - 50])
