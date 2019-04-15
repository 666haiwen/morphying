import numpy as np
import cv2 as cv
import os
from morphing import Morphing
from utils import ImageWindow
from matplotlib import pyplot as plt
from matplotlib import image as mpimg


module_dir = os.path.dirname(__file__)
mophy = Morphing('img/1.bmp', 'img/2.bmp')
src, dst = mophy.srcImg, mophy.dstImg
imgWindow = ImageWindow(src, dst, 'test')
imgWindow.interface_window()
# imgList = mophy.cross_dissolve(alpha=0.05)
# mophy.save_Gifs('1.gif')
