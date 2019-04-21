import numpy as np
import cv2 as cv
import imageio
from const import RESULT_DIR


def cross_dissolve(imgSrc, imgDst, interval=0.05):
    """
        morphing by cross_dissolve
        @params:
            imgSrc: the source image to transfer
            imgDst: the destinate image to transfer
            interval: the step to close the dst img, default = 0.05
        @return:
            imgList: the list of transfer imgs
    """
    imgList = []
    for alpha in np.arange(0.0, 1.0 + interval, interval):
        tmpImg = np.uint8(imgSrc * (1 - alpha) + imgDst * alpha)
        imgList.append(tmpImg.copy())
    return imgList


def save_Gifs(imgList, name):
    """
        save the result by morphying.
        Such as gif and transfer processing.
    """
    index = 0
    size = imgList[0].shape
    imgTransfer = np.zeros((size[0], size[1] * 6, size[2]))
    path = RESULT_DIR + '/{}.gif'.format(name)
    with imageio.get_writer(path, mode='i', duration=0.1) as writer:
        length = len(imgList)
        middle_res = [int(v * length) for v in [0, 0.2, 0.4, 0.6, 0.8]]
        for i, img in enumerate(imgList):
            if i in middle_res:
                imgTransfer[:, size[1] * index : size[1] * (index + 1)] = img
                index += 1
            writer.append_data(img[:,:,::-1])
    imgTransfer[:, size[1] * index : size[1] * (index + 1)] = imgList[-1]
    path = RESULT_DIR + '/{}_transfer.png'.format(name)
    cv.imwrite(path, imgTransfer)


class ImageWindow(object):
    def __init__(self, src, dst, name):
        # height * width * 3
        self.shape = shape = src.shape
        self.img = np.zeros((shape[0], shape[1] * 2 + 50, shape[2]), np.uint8)
        self.img[:, :shape[1], :] = src
        self.img[:, shape[1] + 50 :, :] = dst
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
            if x < self.shape[1] and self.pre_point != 1:
                self.top_points.append(np.array([x, y]))
                cv.circle(self.img, (x,y), 3, self.color, -1)
                self.pre_point = -1
                if len(self.top_points) % 2 == 0:
                    self.pre_point = 0
                    draw_line(self.top_points[-2:])
            if x > self.shape[1] + 50 and self.pre_point != -1:
                self.down_points.append(np.array([x, y]))
                cv.circle(self.img, (x,y), 3, self.color, -1)
                self.pre_point = 1
                if len(self.down_points) % 2 == 0:
                    self.pre_point = 0
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
        return set_line(self.top_points), set_line(self.down_points, [-self.shape[1] - 50, 0])
