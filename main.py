from morphing import Morphing
from utils import ImageWindow
from const import IMG_DIR


mophy = Morphing(IMG_DIR + '/wyf.jpg', IMG_DIR + '/ph.jpg')
src, dst = mophy.srcImg, mophy.dstImg
imgWindow = ImageWindow(src, dst, 'Morphying')
src_lines, dst_lines = imgWindow.interface_window()
mophy(src_lines, dst_lines, 'hhh')
