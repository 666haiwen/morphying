import numpy as np
import cv2 as cv
import dlib


class FaceFeatures(object):
    """
        get face features by dlib and model pre-trained.
    """
    def __init__(self, model):
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(model)
        self.points = []

    def __call__(self, img):
        rects = self.detector(img, 0)
        self.points = []
        for i in range(len(rects)):
            landmarks = np.matrix([[p.x, p.y] for p in self.predictor(img, rects[i]).parts()])
            for idx, point in enumerate(landmarks):
                pos = (point[0, 0], point[0, 1])
                self.points.append(pos)
        # height * width
        y, x = img.shape[0], img.shape[1]
        y_m, x_m = int(y / 2), int(x / 2)
        self.points += [(0, 0), (x_m, 0), (x - 1, 0),\
            (0, y_m), (x - 1, y_m),\
            (0, y - 1), (x_m, y - 1), (x - 1, y - 1)]
        return self.points


class FaceMorphing(object):
    def __init__(self, img_src, img_dst, model):
        features = FaceFeatures(model)
        self.points_src = features(cv.cvtColor(img_src, cv.COLOR_BGR2GRAY))
        self.points_dst = features(cv.cvtColor(img_dst, cv.COLOR_BGR2GRAY))
        self.img_src = np.float32(img_src)
        self.img_dst = np.float32(img_dst)
        self.tri_list = self.get_tri(img_src.shape, self.points_src)
        self.t_src, self.t_dst = [], []
        for x, y, z in self.tri_list:
            self.t_src.append([self.points_src[x], self.points_src[y], self.points_src[z]])
            self.t_dst.append([self.points_dst[x], self.points_dst[y], self.points_dst[z]])

    def get_tri(self, size, points):
        """
            get Delaunay Triangulation.
            @params:
                size: shape of imgs
                points: feature points of face
            @return:
                triList: index of triangle points in parmas points
        """
        rect = (0, 0, size[1], size[0])
        subdiv = cv.Subdiv2D(rect)
        for p in points :
            subdiv.insert(p)
        tri_points = subdiv.getTriangleList()
        tri_list = [[points.index((t[0], t[1])), points.index((t[2], t[3])),\
            points.index((t[4], t[5]))] for t in tri_points]
        return tri_list


    def applyAffineTransform(self, src, tri_src, tri_dst, size) :
        warpMat = cv.getAffineTransform(np.float32(tri_src), np.float32(tri_dst))
        return cv.warpAffine(src, warpMat, (size[0], size[1]), None,\
            flags=cv.INTER_LINEAR, borderMode=cv.BORDER_REFLECT_101)


    def morphTriangle(self, img, t_src, t_dst, t, alpha) :
        """
            blends triangular regions from img_src and img_dst to img by warps and alpha.
            @params:
                img: blending result
                t_src: triangular regions of src img
                t_dst: triangular regions of dst img
                t: triangular regions of blending img
                alpha: alpha value
        """
        r_src = cv.boundingRect(np.float32([t_src]))
        r_dst = cv.boundingRect(np.float32([t_dst]))
        r = cv.boundingRect(np.float32([t]))

        # Offset points by left top corner of the respective rectangles
        t_src_Rect = []
        t_dst_Rect = []
        t_Rect = []
        for i in range(0, 3):
            t_Rect.append(((t[i][0] - r[0]), (t[i][1] - r[1])))
            t_src_Rect.append(((t_src[i][0] - r_src[0]), (t_src[i][1] - r_src[1])))
            t_dst_Rect.append(((t_dst[i][0] - r_dst[0]), (t_dst[i][1] - r_dst[1])))

        # Get mask by filling triangle
        mask = np.zeros((r[3], r[2], 3), dtype = np.float32)
        cv.fillConvexPoly(mask, np.int32(t_Rect), (1.0, 1.0, 1.0), 16, 0);

        img_srcRect = self.img_src[r_src[1]:r_src[1] + r_src[3], r_src[0]:r_src[0] + r_src[2]]
        img_dstRect = self.img_dst[r_dst[1]:r_dst[1] + r_dst[3], r_dst[0]:r_dst[0] + r_dst[2]]

        size = (r[2], r[3])
        warpImage_src = self.applyAffineTransform(img_srcRect, t_src_Rect, t_Rect, size)
        warpImage_dst = self.applyAffineTransform(img_dstRect, t_dst_Rect, t_Rect, size)

        imgRect = (1.0 - alpha) * warpImage_src + alpha * warpImage_dst
        img[r[1]:r[1]+r[3], r[0]:r[0]+r[2]] = img[r[1]:r[1]+r[3], r[0]:r[0]+r[2]] * ( 1 - mask ) + imgRect * mask


    def __call__(self, interval):
        morphRes = []
        for alpha in np.arange(0, 1 + interval, interval):
            points = [];
            for i in range(0, len(self.points_src)):
                x = ( 1 - alpha ) * self.points_src[i][0] + alpha * self.points_dst[i][0]
                y = ( 1 - alpha ) * self.points_src[i][1] + alpha * self.points_dst[i][1]
                points.append((x,y))
            morph_frame = np.zeros(self.img_src.shape, dtype = self.img_src.dtype)
            for i, (x, y, z) in enumerate(self.tri_list):
                t_morph = [points[x], points[y], points[z]]
                self.morphTriangle(morph_frame, self.t_src[i], self.t_dst[i], t_morph, alpha)
            morphRes.append(np.uint8(morph_frame))
        return morphRes
