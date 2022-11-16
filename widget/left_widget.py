from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ui.main_form import *
from utils import common, style_sheet


class LeftWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(LeftWidget, self).__init__(parent)
        leftLayout = QVBoxLayout()

        self.setLayout(leftLayout)
        self.setMinimumWidth(300)
        self.setMaximumHeight(600)

        self.btnCreateVideo = QPushButton("動画作成")
        self.btnCreateVideo.setIcon(QIcon("./data/video.png"))

        common.set_shadow(self.btnCreateVideo)
        self.btnCreateVideo.setStyleSheet(style_sheet.QPushButtonStyle())
        self.btnCreateVideo.setMinimumSize(100, 100)

        self.btnCreateDataset = QPushButton("データセット作成")
        common.set_shadow(self.btnCreateDataset)
        self.btnCreateDataset.setStyleSheet(style_sheet.QPushButtonStyle())
        self.btnCreateDataset.setMinimumSize(100, 100)

        self.btn_ai_start = QPushButton("AI開始")
        common.set_shadow(self.btn_ai_start)
        self.btn_ai_start.setStyleSheet(style_sheet.QPushButtonStyle())
        self.btn_ai_start.setMinimumSize(100, 100)

        leftLayout.addWidget(self.btnCreateVideo, 0, QtCore.Qt.AlignVCenter)
        leftLayout.addWidget(self.btnCreateDataset, 0, QtCore.Qt.AlignVCenter)
        leftLayout.addWidget(self.btn_ai_start, 0, QtCore.Qt.AlignVCenter)
