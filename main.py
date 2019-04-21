import os
import cv2 as cv
from morphing import Morphing
from face import FaceMorphing
from utils import ImageWindow, cross_dissolve, save_Gifs
from const import IMG_DIR, INTERVAL, MODEL_DIR


if __name__ == '__main__' :
    # get image
    img_src = cv.imread(IMG_DIR + '/1.bmp')
    img_dst = cv.imread(IMG_DIR + '/2.bmp')

    # cross dissolve method
    imgList = cross_dissolve(img_src, img_dst, INTERVAL)
    save_Gifs(imgList, 'cross_dissolve')
    print('Finish cross dissovle method!')

    # face features method
    face = FaceMorphing(img_src, img_dst, os.path.join(MODEL_DIR, 'shape_predictor_68_face_landmarks.dat'))
    save_Gifs(face(INTERVAL), 'face_features')
    print('Finish face features method!')

    # feature-based Image Metamorphosis method
    mophy = Morphing(img_src, img_dst)
    imgWindow = ImageWindow(img_src, img_dst, 'Morphying')
    src_lines, dst_lines = imgWindow.interface_window()
    save_Gifs(mophy(src_lines, dst_lines, INTERVAL), 'mult_lines')
    print('Finish mult-features-lines method!')
