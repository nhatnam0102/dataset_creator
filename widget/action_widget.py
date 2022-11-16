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


class ActionWidget(QtWidgets.QWidget):
    def __init__(self):
        super(ActionWidget, self).__init__()
        self.create_ui()

    def create_ui(self):
        main_layout = QVBoxLayout()
        information_widget = QGroupBox()
        information_widget.setStyleSheet(style_sheet.QGroupBoxStyle2())
        information_layout = QHBoxLayout()
        self.lb_center = QLabel("YAKULT Center")
        self.lb_center.setStyleSheet(style_sheet.QLabelStyle())
        self.lb_yl_id = QLabel("担当者ID- XXXXXXXXXX")
        self.lb_yl_id.setStyleSheet(style_sheet.QLabelStyle())
        self.lb_yl_name = QLabel("担当者名- XXXXXXXXXX")
        self.lb_yl_name.setStyleSheet(style_sheet.QLabelStyle())

        information_layout.addWidget(self.lb_center)
        information_layout.addWidget(self.lb_yl_id)
        information_layout.addWidget(self.lb_yl_name)

        information_widget.setLayout(information_layout)

        action_widget = QtWidgets.QWidget()
        action_layout = QGridLayout()

        self.action_1 = QToolButton()
        common.set_shadow(self.action_1)
        self.action_1.setText("ACTION 1")
        self.action_1.setStyleSheet(
            style_sheet.QToolButtonStyle(padding_top=0, border_radius=15, margin_left=15))

        self.action_2 = QToolButton()
        common.set_shadow(self.action_2)
        self.action_2.setText("ACTION 2")
        self.action_2.setStyleSheet(
            style_sheet.QToolButtonStyle(padding_top=0, border_radius=15, margin_left=15))

        self.action_3 = QToolButton()
        common.set_shadow(self.action_3)
        self.action_3.setText("ACTION 3")
        self.action_3.setStyleSheet(
            style_sheet.QToolButtonStyle(padding_top=0, border_radius=15, margin_left=15))

        self.action_4 = QToolButton()
        common.set_shadow(self.action_4)
        self.action_4.setText("ACTION 4")
        self.action_4.setStyleSheet(
            style_sheet.QToolButtonStyle(padding_top=0, border_radius=15, margin_left=15))

        self.action_5 = QToolButton()
        common.set_shadow(self.action_5)
        self.action_5.setText("ACTION 5")
        self.action_5.setStyleSheet(
            style_sheet.QToolButtonStyle(padding_top=0, border_radius=15, margin_left=15))

        self.action_6 = QToolButton()
        common.set_shadow(self.action_6)
        self.action_6.setText("ACTION 6")
        self.action_6.setStyleSheet(
            style_sheet.QToolButtonStyle(padding_top=0, border_radius=15, margin_left=15))

        self.action_7 = QToolButton()
        common.set_shadow(self.action_7)
        self.action_7.setText("ACTION 7")
        self.action_7.setStyleSheet(
            style_sheet.QToolButtonStyle(padding_top=0, border_radius=15, margin_left=15))

        self.action_8 = QToolButton()
        common.set_shadow(self.action_8)
        self.action_8.setText("ACTION 7")
        self.action_8.setStyleSheet(
            style_sheet.QToolButtonStyle(padding_top=0, border_radius=15, margin_left=15))

        self.action_9 = QToolButton()
        common.set_shadow(self.action_9)
        self.action_9.setText("ACTION 9")
        self.action_9.setStyleSheet(
            style_sheet.QToolButtonStyle(padding_top=0, border_radius=15, margin_left=15))

        self.action_10 = QToolButton()
        common.set_shadow(self.action_10)
        self.action_10.setText("ACTION 10")
        self.action_10.setStyleSheet(
            style_sheet.QToolButtonStyle(padding_top=0, border_radius=15, margin_left=15))

        self.action_11 = QToolButton()
        common.set_shadow(self.action_11)
        self.action_11.setText("ACTION 11")
        self.action_11.setStyleSheet(
            style_sheet.QToolButtonStyle(padding_top=0, border_radius=15, margin_left=15))

        action_layout.setSpacing(100)
        action_layout.addWidget(self.action_1, 1, 1)
        action_layout.addWidget(self.action_2, 1, 2)
        action_layout.addWidget(self.action_3, 1, 3)
        action_layout.addWidget(self.action_4, 2, 1)
        action_layout.addWidget(self.action_5, 2, 2)
        action_layout.addWidget(self.action_6, 3, 1)
        action_layout.addWidget(self.action_7, 3, 2)
        action_layout.addWidget(self.action_8, 3, 3)
        action_layout.addWidget(self.action_9, 3, 4)
        action_layout.addWidget(self.action_10, 4, 1)
        action_layout.addWidget(self.action_11, 4, 2)


        action_widget.setLayout(action_layout)

        bottom_widget = QtWidgets.QWidget()
        bottom_layout = QHBoxLayout()

        self.back = QToolButton()
        common.set_shadow(self.back)
        self.back.setText("戻る")
        self.back.setMaximumHeight(100)
        self.back.setMaximumWidth(150)

        self.back.setStyleSheet(
            style_sheet.QToolButtonStyle(padding_top=0, border_radius=15, margin_left=15,width=150,height=100))

        self.com = QComboBox()
        self.com.setMaximumWidth(900)
        self.com.setStyleSheet(style_sheet.QComboBoxStyle(height=100,border_radius=15))

        self.next = QToolButton()
        common.set_shadow(self.next)
        self.next.setText("次へ")
        self.next.setStyleSheet(
            style_sheet.QToolButtonStyle(padding_top=0, border_radius=15, margin_left=15))

        bottom_layout.addWidget(self.back)
        bottom_layout.addWidget(self.com)
        bottom_layout.addWidget(self.next)

        bottom_widget.setLayout(bottom_layout)

        main_layout.addWidget(information_widget, 2, QtCore.Qt.AlignTop)
        main_layout.addWidget(action_widget, 6, QtCore.Qt.AlignTop)
        main_layout.addWidget(bottom_widget, 2, QtCore.Qt.AlignTop)
        self.setLayout(main_layout)
