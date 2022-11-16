import random
import time

import cv2
import os
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import threading
from widget.right_widget import RightWidget

from utils import img_proc, common, style_sheet
from constants import *
import logging


class TrainModelWidget(QtWidgets.QWidget):
    def __init__(self):
        super(TrainModelWidget, self).__init__()
