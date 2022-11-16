import time

import cv2
import os
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets,QtSvg
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import threading
import utils.common
from utils import img_proc, common, style_sheet
from constants import *


class InitWidget(QtWidgets.QWidget):
    def __init__(self):
        super(InitWidget, self).__init__()
        introLayout = QVBoxLayout()
        logo = QLabel("DATASET GENERATOR")
        logo.setStyleSheet(style_sheet.QLabelStyle(font_size=50))
        self.loading = QtSvg.QSvgWidget("./data/resource/200px.svg")

        introLayout.addWidget(logo, 8, QtCore.Qt.AlignCenter)
        introLayout.addWidget(self.loading, 2, QtCore.Qt.AlignCenter)
        self.setLayout(introLayout)
