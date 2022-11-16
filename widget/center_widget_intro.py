import time

import cv2
import os
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import threading
import utils.common
from utils import img_proc, common, style_sheet
from constants import *


class Intro(QtWidgets.QWidget):
    def __init__(self):
        super(Intro, self).__init__()
        intro_layout = QHBoxLayout()
        logo = QLabel()
        img = cv2.imread("./data/resource/img.png")
        logo.setPixmap(common.get_pixmap(img))
        intro_layout.addWidget(logo, 0, QtCore.Qt.AlignCenter)
        self.setLayout(intro_layout)
