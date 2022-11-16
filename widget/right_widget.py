import time

import cv2
import os
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import threading


class RightWidget(QtWidgets.QWidget):
    def __init__(self):
        super(RightWidget, self).__init__()
        rightLayout = QVBoxLayout()
        with open("./data/names35.txt", 'r', encoding="UTF-8") as f:
            list_yakult = [line.strip() for line in f]
        with open("./data/class_names_by_id.txt", 'r', encoding="UTF-8") as f:
            self.list_folder_yk = [line.strip() for line in f]
        self.listWidget = QListWidget()
        self.listWidget.addItems(list_yakult)
        rightLayout.addWidget(self.listWidget)
        self.setLayout(rightLayout)

    def get_current_item(self):
        return self.listWidget.currentRow(), self.listWidget.currentItem().text(), self.list_folder_yk[
            int(self.listWidget.currentRow())]
